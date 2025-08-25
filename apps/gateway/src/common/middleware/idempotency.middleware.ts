import { Injectable, NestMiddleware, HttpException, HttpStatus } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { RedisService } from '../../redis/redis.service';

@Injectable()
export class IdempotencyMiddleware implements NestMiddleware {
  constructor(private readonly redisService: RedisService) {}

  async use(req: Request, res: Response, next: NextFunction) {
    const idempotencyKey = req.headers['idempotency-key'] as string;
    
    // Only apply to mutation methods
    if (!['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
      return next();
    }

    if (!idempotencyKey) {
      throw new HttpException(
        'Idempotency-Key header is required for mutation operations',
        HttpStatus.BAD_REQUEST
      );
    }

    // Check if we've already processed this request
    const cacheKey = `idempotency:${idempotencyKey}`;
    const cachedResponse = await this.redisService.get(cacheKey);

    if (cachedResponse) {
      const response = JSON.parse(cachedResponse);
      return res.status(response.status).json(response.data);
    }

    // Store the original response methods
    const originalJson = res.json;
    const originalStatus = res.status;

    let responseData: any;
    let responseStatus: number;

    // Override response.json to capture the response
    res.json = function(data: any) {
      responseData = data;
      return originalJson.call(this, data);
    };

    // Override response.status to capture the status
    res.status = function(status: number) {
      responseStatus = status;
      return originalStatus.call(this, status);
    };

    // Store the response after the request is processed
    res.on('finish', async () => {
      if (responseStatus >= 200 && responseStatus < 300) {
        const responseToCache = {
          status: responseStatus,
          data: responseData,
        };
        
        // Cache for 24 hours
        await this.redisService.set(
          cacheKey,
          JSON.stringify(responseToCache),
          86400
        );
      }
    });

    next();
  }
}
