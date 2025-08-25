import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';
import { Organization } from './entities/organization.entity';
import { Membership } from './entities/membership.entity';
import { Plan } from './entities/plan.entity';
import { Scenario } from './entities/scenario.entity';
import { SiteBoundary } from './entities/site-boundary.entity';
import { Parcel } from './entities/parcel.entity';
import { Link } from './entities/link.entity';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      User,
      Organization,
      Membership,
      Plan,
      Scenario,
      SiteBoundary,
      Parcel,
      Link,
    ]),
  ],
  exports: [TypeOrmModule],
})
export class DatabaseModule {}
