import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne, OneToMany } from 'typeorm';
import { Organization } from './organization.entity';
import { Scenario } from './scenario.entity';

@Entity('plans')
export class Plan {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;

  @Column({ nullable: true })
  description: string;

  @ManyToOne(() => Organization, organization => organization.plans)
  organization: Organization;

  @Column()
  organizationId: string;

  @Column({ type: 'jsonb', nullable: true })
  brief: {
    targetPopulation?: number;
    targetJobs?: number;
    landUseGoals?: Record<string, number>;
    affordabilityPercent?: number;
    heightCaps?: number;
    farCaps?: number;
    parkingPolicy?: string;
    modeShareTargets?: Record<string, number>;
    renewableEnergyTarget?: number;
    waterReuseTarget?: number;
    ghgBudget?: number;
  };

  @Column({ type: 'jsonb', nullable: true })
  constraints: {
    regulatoryOverlays?: any[];
    hazardousBuffers?: any[];
    easements?: any[];
    historicDistricts?: any[];
  };

  @Column({ type: 'jsonb', nullable: true })
  contextData: {
    baseMapTiles?: string;
    osmExtracts?: any[];
    backgroundDemand?: any[];
    costLibraries?: any[];
  };

  @Column({ default: 'draft' })
  status: 'draft' | 'in_progress' | 'review' | 'approved' | 'archived';

  @OneToMany(() => Scenario, scenario => scenario.plan)
  scenarios: Scenario[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ nullable: true })
  createdBy: string;

  @Column({ nullable: true })
  updatedBy: string;
}
