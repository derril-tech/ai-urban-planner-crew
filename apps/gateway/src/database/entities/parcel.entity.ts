import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne } from 'typeorm';
import { Scenario } from './scenario.entity';

@Entity('parcels')
export class Parcel {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => Scenario, scenario => scenario.parcels)
  scenario: Scenario;

  @Column()
  scenarioId: string;

  @Column({ type: 'geometry', srid: 4326 })
  geometry: any; // PostGIS Polygon

  @Column({ type: 'jsonb' })
  properties: {
    useMix: Record<string, number>; // residential: 0.6, commercial: 0.3, etc.
    far: number; // Floor Area Ratio
    height: number; // Building height in meters
    setbacks: Record<string, number>; // front: 3, side: 1.5, rear: 3
    inclusionary: number; // Percentage of affordable units
    phase: number; // Development phase
    lotCoverage: number; // Percentage of lot covered by building
    groundFloorActivation: boolean; // Active ground floor
    parkingRatio: number; // Parking spaces per unit
    density: number; // Units per hectare
  };

  @Column({ type: 'jsonb', nullable: true })
  capacity: {
    units: number;
    population: number;
    jobs: number;
    floorArea: number;
    parkingSpaces: number;
  };

  @Column({ type: 'jsonb', nullable: true })
  utilities: {
    solarPotential?: number; // kWp
    waterDemand?: number; // L/day
    wasteGeneration?: number; // kg/day
    energyDemand?: number; // kWh/day
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
