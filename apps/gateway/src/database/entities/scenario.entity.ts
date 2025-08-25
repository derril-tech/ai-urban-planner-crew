import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne, OneToMany } from 'typeorm';
import { Plan } from './plan.entity';
import { SiteBoundary } from './site-boundary.entity';
import { Parcel } from './parcel.entity';
import { Link } from './link.entity';

@Entity('scenarios')
export class Scenario {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;

  @Column({ nullable: true })
  description: string;

  @ManyToOne(() => Plan, plan => plan.scenarios)
  plan: Plan;

  @Column()
  planId: string;

  @Column({ type: 'jsonb', nullable: true })
  parameters: {
    affordabilityPercent?: number;
    farCaps?: number;
    parkingRatios?: Record<string, number>;
    pvCoverage?: number;
    greenRoofPercent?: number;
    bikeLaneKm?: number;
    treeCanopyPercent?: number;
  };

  @Column({ type: 'jsonb', nullable: true })
  kpis: {
    population?: number;
    jobs?: number;
    vmt?: number;
    modeShare?: Record<string, number>;
    accessIndex?: number;
    sustainabilityScore?: number;
    capex?: number;
    opex?: number;
  };

  @Column({ default: 'draft' })
  status: 'draft' | 'in_progress' | 'completed' | 'archived';

  @Column({ default: false })
  isBaseline: boolean;

  @OneToMany(() => SiteBoundary, boundary => boundary.scenario)
  siteBoundaries: SiteBoundary[];

  @OneToMany(() => Parcel, parcel => parcel.scenario)
  parcels: Parcel[];

  @OneToMany(() => Link, link => link.scenario)
  links: Link[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ nullable: true })
  createdBy: string;

  @Column({ nullable: true })
  updatedBy: string;
}
