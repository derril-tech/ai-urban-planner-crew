import { IsString, IsOptional, IsObject, IsNumber, IsEnum, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class BriefDto {
  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  targetPopulation?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  targetJobs?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsObject()
  landUseGoals?: Record<string, number>;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  affordabilityPercent?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  heightCaps?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  farCaps?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  parkingPolicy?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsObject()
  modeShareTargets?: Record<string, number>;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  renewableEnergyTarget?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  waterReuseTarget?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  ghgBudget?: number;
}

export class ConstraintsDto {
  @ApiPropertyOptional()
  @IsOptional()
  regulatoryOverlays?: any[];

  @ApiPropertyOptional()
  @IsOptional()
  hazardousBuffers?: any[];

  @ApiPropertyOptional()
  @IsOptional()
  easements?: any[];

  @ApiPropertyOptional()
  @IsOptional()
  historicDistricts?: any[];
}

export class ContextDataDto {
  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  baseMapTiles?: string;

  @ApiPropertyOptional()
  @IsOptional()
  osmExtracts?: any[];

  @ApiPropertyOptional()
  @IsOptional()
  backgroundDemand?: any[];

  @ApiPropertyOptional()
  @IsOptional()
  costLibraries?: any[];
}

export class CreatePlanDto {
  @ApiProperty({ description: 'Plan name' })
  @IsString()
  name: string;

  @ApiPropertyOptional({ description: 'Plan description' })
  @IsOptional()
  @IsString()
  description?: string;

  @ApiPropertyOptional({ description: 'Planning brief' })
  @IsOptional()
  @ValidateNested()
  @Type(() => BriefDto)
  brief?: BriefDto;

  @ApiPropertyOptional({ description: 'Planning constraints' })
  @IsOptional()
  @ValidateNested()
  @Type(() => ConstraintsDto)
  constraints?: ConstraintsDto;

  @ApiPropertyOptional({ description: 'Context data' })
  @IsOptional()
  @ValidateNested()
  @Type(() => ContextDataDto)
  contextData?: ContextDataDto;
}
