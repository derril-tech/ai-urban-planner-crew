import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne, OneToMany } from 'typeorm';
import { Organization } from './organization.entity';
import { Membership } from './membership.entity';

export enum UserRole {
  OWNER = 'owner',
  ADMIN = 'admin',
  PLANNER = 'planner',
  DESIGNER = 'designer',
  ANALYST = 'analyst',
  FACILITATOR = 'facilitator',
  VIEWER = 'viewer'
}

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  email: string;

  @Column({ nullable: true })
  name: string;

  @Column({ nullable: true })
  avatar: string;

  @Column({ type: 'enum', enum: UserRole, default: UserRole.VIEWER })
  role: UserRole;

  @Column({ default: false })
  emailVerified: boolean;

  @Column({ nullable: true })
  passwordHash: string;

  @Column({ type: 'jsonb', nullable: true })
  oauthProviders: Record<string, any>;

  @ManyToOne(() => Organization, organization => organization.users)
  organization: Organization;

  @Column()
  organizationId: string;

  @OneToMany(() => Membership, membership => membership.user)
  memberships: Membership[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ nullable: true })
  lastLoginAt: Date;
}
