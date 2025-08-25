import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne } from 'typeorm';
import { User } from './user.entity';
import { Organization } from './organization.entity';

export enum MembershipRole {
  OWNER = 'owner',
  ADMIN = 'admin',
  PLANNER = 'planner',
  DESIGNER = 'designer',
  ANALYST = 'analyst',
  FACILITATOR = 'facilitator',
  VIEWER = 'viewer'
}

@Entity('memberships')
export class Membership {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @ManyToOne(() => User, user => user.memberships)
  user: User;

  @Column()
  userId: string;

  @ManyToOne(() => Organization, organization => organization.users)
  organization: Organization;

  @Column()
  organizationId: string;

  @Column({ type: 'enum', enum: MembershipRole, default: MembershipRole.VIEWER })
  role: MembershipRole;

  @Column({ type: 'jsonb', nullable: true })
  permissions: Record<string, boolean>;

  @Column({ default: true })
  isActive: boolean;

  @Column({ nullable: true })
  invitedBy: string;

  @Column({ nullable: true })
  acceptedAt: Date;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
