import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne } from 'typeorm';
import { Scenario } from './scenario.entity';

export enum LinkClass {
  ARTERIAL = 'arterial',
  COLLECTOR = 'collector',
  LOCAL = 'local',
  PED_MALL = 'ped_mall',
  CYCLEWAY = 'cycleway',
  TRANSIT = 'transit'
}

@Entity('links')
export class Link {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => Scenario, scenario => scenario.links)
  scenario: Scenario;

  @Column()
  scenarioId: string;

  @Column({ type: 'geometry', srid: 4326 })
  geometry: any; // PostGIS LineString

  @Column({ type: 'enum', enum: LinkClass })
  linkClass: LinkClass;

  @Column({ type: 'jsonb' })
  properties: {
    name?: string;
    length: number; // meters
    width: number; // meters
    lanes: number;
    speedLimit: number; // km/h
    transitPriority: boolean;
    bikeLane: boolean;
    sidewalk: boolean;
    parking: boolean;
    turnRestrictions?: Record<string, string[]>;
    transitStops?: any[];
    bikeDocks?: any[];
  };

  @Column({ type: 'jsonb', nullable: true })
  performance: {
    capacity?: number; // vehicles per hour
    levelOfService?: string; // A-F
    bikeLevelOfService?: string; // A-F
    pedestrianLevelOfService?: string; // A-F
    transitFrequency?: number; // buses per hour
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
