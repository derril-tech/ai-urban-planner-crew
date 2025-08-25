import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne } from 'typeorm';
import { Scenario } from './scenario.entity';

@Entity('site_boundaries')
export class SiteBoundary {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => Scenario, scenario => scenario.siteBoundaries)
  scenario: Scenario;

  @Column()
  scenarioId: string;

  @Column({ type: 'geometry', srid: 4326 })
  geometry: any; // PostGIS Polygon/MultiPolygon

  @Column({ type: 'jsonb', nullable: true })
  properties: {
    name?: string;
    area?: number;
    perimeter?: number;
    elevation?: number;
    slope?: number;
    existingUse?: string;
    zoning?: string;
  };

  @Column({ type: 'jsonb', nullable: true })
  contextLayers: {
    floodZones?: any[];
    wetlands?: any[];
    protectedAreas?: any[];
    existingParcels?: any[];
    rightOfWay?: any[];
    protectedTrees?: any[];
  };

  @Column({ default: 'active' })
  status: 'active' | 'inactive' | 'deleted';

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ nullable: true })
  createdBy: string;

  @Column({ nullable: true })
  updatedBy: string;
}
