import {
  ExceptionFilter,
  Catch,
  ArgumentsHost,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { Request, Response } from 'express';

export interface ProblemJson {
  type: string;
  title: string;
  status: number;
  detail?: string;
  instance?: string;
  errors?: Record<string, string[]>;
}

@Catch()
export class ProblemJsonFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status = HttpStatus.INTERNAL_SERVER_ERROR;
    let title = 'Internal Server Error';
    let detail: string | undefined;
    let errors: Record<string, string[]> | undefined;

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      const exceptionResponse = exception.getResponse() as any;
      
      title = exceptionResponse.message || exception.message;
      detail = exceptionResponse.error || exception.message;
      
      if (exceptionResponse.message && Array.isArray(exceptionResponse.message)) {
        errors = this.formatValidationErrors(exceptionResponse.message);
      }
    } else if (exception instanceof Error) {
      detail = exception.message;
    }

    const problemJson: ProblemJson = {
      type: `https://api.urban-planner.com/problems/${status}`,
      title,
      status,
      detail,
      instance: request.url,
    };

    if (errors) {
      problemJson.errors = errors;
    }

    response
      .status(status)
      .json(problemJson);
  }

  private formatValidationErrors(messages: string[]): Record<string, string[]> {
    const errors: Record<string, string[]> = {};
    
    messages.forEach(message => {
      const match = message.match(/^([^.]+)\.([^:]+): (.+)$/);
      if (match) {
        const [, object, field, error] = match;
        const key = `${object}.${field}`;
        if (!errors[key]) {
          errors[key] = [];
        }
        errors[key].push(error);
      } else {
        if (!errors['general']) {
          errors['general'] = [];
        }
        errors['general'].push(message);
      }
    });

    return errors;
  }
}
