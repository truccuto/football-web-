import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NFLM.settings")
django.setup()

from login.models import GoalType, Nation, Position, Regulation, Sponsor, Stadium, Status
from django.db import models

types = [
    GoalType(typename='Free Kick'),
    GoalType(typename='Penalty'),
    GoalType(typename='Direct'),
    GoalType(typename='Own Goal')
]

GoalType.objects.bulk_create(types)

# Lấy tất cả các bản ghi của mô hình có trường field_name
duplicate_records = GoalType.objects.values('typename').annotate(count=models.Count('typeid')).filter(count__gt=1)

# Lặp qua các bản ghi trùng lặp và xóa bản ghi lặp thứ hai trở đi
for duplicate_record in duplicate_records:
    field_value = duplicate_record['typename']
    duplicate_instances = GoalType.objects.filter(typename=field_value)
    duplicate_instances.exclude(pk=duplicate_instances.first().pk).delete()

nations = [
    Nation(nation_name='Vietnam'),
    Nation(nation_name='Albania'),
    Nation(nation_name='Algeria'),
    Nation(nation_name='Argentina'),
    Nation(nation_name='Australia'),
    Nation(nation_name='Austria'),
    Nation(nation_name='Belgium'),
    Nation(nation_name='Bosnia and Herzegovina'),
    Nation(nation_name='Brazil'),
    Nation(nation_name='Burkina Faso'),
    Nation(nation_name='Cameroon'),
    Nation(nation_name='Colombia'),
    Nation(nation_name='Congo DR'),
    Nation(nation_name='Costa Rica'),
    Nation(nation_name='Croatia'),
    Nation(nation_name='Côte d`Ivoire'),
    Nation(nation_name='Czech Republic'),
    Nation(nation_name='Denmark'),
    Nation(nation_name='Ecuador'),
    Nation(nation_name='Egypt'),
    Nation(nation_name='England'),
    Nation(nation_name='Estonia'),
    Nation(nation_name='Finland'),
    Nation(nation_name='France'),
    Nation(nation_name='Gabon'),
    Nation(nation_name='Germany'),
    Nation(nation_name='Ghana'),
    Nation(nation_name='Greece'),
    Nation(nation_name='Grenada'),
    Nation(nation_name='Guinea'),
    Nation(nation_name='IR Iran'),
    Nation(nation_name='Iraq'),
    Nation(nation_name='Israel'),
    Nation(nation_name='Italy'),
    Nation(nation_name='Jamaica'),
    Nation(nation_name='Japan'),
    Nation(nation_name='Korea Republic'),
    Nation(nation_name='Liberia'),
    Nation(nation_name='Mexico'),
    Nation(nation_name='Mali'),
    Nation(nation_name='Montenegro'),
    Nation(nation_name='Montserrat'),
    Nation(nation_name='Morocco'),
    Nation(nation_name='Netherlands'),
    Nation(nation_name='New Zealand'),
    Nation(nation_name='Nigeria'),
    Nation(nation_name='Northern Ireland'),
    Nation(nation_name='Norway'),
    Nation(nation_name='Paraguay'),
    Nation(nation_name='Poland'),
    Nation(nation_name='Portugal'),
    Nation(nation_name='Republic of Ireland'),
    Nation(nation_name='Senegal'),
    Nation(nation_name='Scotland'),
    Nation(nation_name='Serbia'),
    Nation(nation_name='Slovakia'),
    Nation(nation_name='Spain'),
    Nation(nation_name='Sweden'),
    Nation(nation_name='Switzerland'),
    Nation(nation_name='Tunisia'),
    Nation(nation_name='Turkiye'),
    Nation(nation_name='Ukraine'),
    Nation(nation_name='United States'),
    Nation(nation_name='Uruguay'),
    Nation(nation_name='Venezuela'),
    Nation(nation_name='Wales'),
    Nation(nation_name='Zambia'),
    Nation(nation_name='Zimbabwe'),
]

Nation.objects.bulk_create(nations)

# Lấy tất cả các bản ghi của mô hình có trường field_name
duplicate_records = Nation.objects.values('nation_name').annotate(count=models.Count('nationid')).filter(count__gt=1)

# Lặp qua các bản ghi trùng lặp và xóa bản ghi lặp thứ hai trở đi
for duplicate_record in duplicate_records:
    field_value = duplicate_record['nation_name']
    duplicate_instances = Nation.objects.filter(nation_name=field_value)
    duplicate_instances.exclude(pk=duplicate_instances.first().pk).delete()

positions = [
    Position(positionname='Goalkeeper'),
    Position(positionname='Defender'),
    Position(positionname='Midfielder'),
    Position(positionname='Forward'),
]

Position.objects.bulk_create(positions)

# Lấy tất cả các bản ghi của mô hình có trường field_name
duplicate_records = Position.objects.values('positionname').annotate(count=models.Count('positionid')).filter(count__gt=1)

# Lặp qua các bản ghi trùng lặp và xóa bản ghi lặp thứ hai trở đi
for duplicate_record in duplicate_records:
    field_value = duplicate_record['positionname']
    duplicate_instances = Position.objects.filter(positionname=field_value)
    duplicate_instances.exclude(pk=duplicate_instances.first().pk).delete()

Regulation.objects.create()

sponsors = [
    Sponsor(sponsor_name='sponsors_1'),
    Sponsor(sponsor_name='sponsors_2'),
    Sponsor(sponsor_name='sponsors_3'),
    Sponsor(sponsor_name='sponsors_4'),
    Sponsor(sponsor_name='N/A'),
]

Sponsor.objects.bulk_create(sponsors)

# Lấy tất cả các bản ghi của mô hình có trường field_name
duplicate_records = Sponsor.objects.values('sponsor_name').annotate(count=models.Count('sponsorid')).filter(count__gt=1)

# Lặp qua các bản ghi trùng lặp và xóa bản ghi lặp thứ hai trở đi
for duplicate_record in duplicate_records:
    field_value = duplicate_record['sponsor_name']
    duplicate_instances = Sponsor.objects.filter(sponsor_name=field_value)
    duplicate_instances.exclude(pk=duplicate_instances.first().pk).delete()

stadiums = []
stadiums = [
    Stadium(name='Lạch Tray'),
    Stadium(name='Hàng Đẫy'),
    Stadium(name='Quy Nhơn'),
    Stadium(name='Ninh Bình'),
    Stadium(name='Hoà Xuân'),
    Stadium(name='Buôn Ma Thuột'),
    Stadium(name='Mỹ Đình'),
    Stadium(name='Thiên Trường'),
    Stadium(name='Cần Thơ'),
    Stadium(name='Chi Lăng'),
    Stadium(name='Tự do'),
    Stadium(name='Hà Nam'),
    Stadium(name='Thống Nhất'),
    Stadium(name='Hà Tĩnh'),

]

Stadium.objects.bulk_create(stadiums)

# Lấy tất cả các bản ghi của mô hình có trường field_name
duplicate_records = Stadium.objects.values('name').annotate(count=models.Count('stadiumid')).filter(count__gt=1)

# Lặp qua các bản ghi trùng lặp và xóa bản ghi lặp thứ hai trở đi
for duplicate_record in duplicate_records:
    field_value = duplicate_record['name']
    duplicate_instances = Stadium.objects.filter(name=field_value)
    duplicate_instances.exclude(pk=duplicate_instances.first().pk).delete()


statuses = [
    Status(statusname='Upcoming'),
    Status(statusname='Done'),
]

Status.objects.bulk_create(statuses)

# Lấy tất cả các bản ghi của mô hình có trường field_name
duplicate_records = Status.objects.values('statusname').annotate(count=models.Count('statusid')).filter(count__gt=1)

# Lặp qua các bản ghi trùng lặp và xóa bản ghi lặp thứ hai trở đi
for duplicate_record in duplicate_records:
    field_value = duplicate_record['statusname']
    duplicate_instances = Status.objects.filter(statusname=field_value)
    duplicate_instances.exclude(pk=duplicate_instances.first().pk).delete()