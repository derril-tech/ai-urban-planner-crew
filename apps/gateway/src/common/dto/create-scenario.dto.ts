import { IsString, IsOptional, IsObject, IsNumber, IsBoolean, ValidateNested } from 'class-validator';
import { Type } from 'class-transformer';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class ParametersDto {
  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  affordabilityPercent?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  farCaps?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsObject()
  parkingRatios?: Record<string, number>;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  pvCoverage?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  greenRoofPercent?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  bikeLaneKm?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  treeCanopyPercent?: number;
}

export class CreateScenarioDto {
  @ApiProperty({ description: 'Scenario name' })
  @IsString()
  name: string;

  @ApiPropertyOptional({ description: 'Scenario description' })
  @IsOptional()
  @IsString()
  description?: string;

  @ApiPropertyOptional({ description: 'Scenario parameters' })
  @IsOptional()
  @ValidateNested()
  @Type(() => ParametersDto)
  parameters?: ParametersDto;

  @ApiPropertyOptional({ description: 'Is baseline scenario' })
  @IsOptional()
  @IsBoolean()
  isBaseline?: boolean;
}
