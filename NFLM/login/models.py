from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    user_type = models.CharField(max_length=20)


class Stadium(models.Model):
    stadiumid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    sponsorid = models.AutoField(primary_key=True)
    sponsor_name = models.CharField(max_length=255)

    def __str__(self):
        return self.sponsor_name


class Nation(models.Model):
    nationid = models.AutoField(primary_key=True)
    nation_name = models.CharField(max_length=255)

    def __str__(self):
        return self.nation_name


class Position(models.Model):
    positionid = models.AutoField(primary_key=True)
    positionname = models.CharField(max_length=20)

    def __str__(self):
        return self.positionname


def get_default_nation():
    nation = Nation.objects.get(nation_name="England")
    return nation


class Team(models.Model):
    teamid = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=255, unique=True)
    team_image = models.ImageField(upload_to="teams_images/", blank=True)
    country = models.ForeignKey(
        Nation, on_delete=models.CASCADE, default=get_default_nation
    )
    status = models.CharField(max_length=255, default="NotMeetRequirements")
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    sponsors = models.ManyToManyField(Sponsor)

    def __str__(self):
        return self.team_name

    def count_local_players(self):
        return self.player_set.filter(nationality=self.country).count()

    def count_foreign_players(self):
        return self.player_set.exclude(nationality=self.country).count()

    def count_total_players(self):
        return self.player_set.count()

    def update_status(self, maxforeignplayer, minplayer, maxplayer):
        foreign_players = self.count_foreign_players()
        total_players = self.count_total_players()
        try:
            coach = Coach.objects.get(team=self)
        except Coach.DoesNotExist:
            coach = None
        if (
            foreign_players <= maxforeignplayer
            and total_players >= minplayer
            and total_players <= maxplayer
            and coach is not None
        ):
            self.status = "MeetRequirements"
        else:
            self.status = "NotMeetRequirements"

        self.save()


class Team_Stat(models.Model):
    teamstatid = models.AutoField(primary_key=True)
    goals = models.PositiveIntegerField(default=0)
    goalsconceded = models.PositiveIntegerField(default=0)
    goaldifference = models.IntegerField(default=0)
    awaygoals = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    loses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    pts = models.PositiveIntegerField(default=0)
    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="team_stat"
    )

    def __str__(self):
        return self.goals


def create_team_stat(sender, instance, created, **kwargs):
    if created:
        Team_Stat.objects.create(team=instance)


post_save.connect(create_team_stat, sender=Team)


class Coach(models.Model):
    coachid = models.AutoField(primary_key=True)
    coach_name = models.CharField(max_length=255)
    nationality = models.ForeignKey(Nation, on_delete=models.CASCADE)
    dob = models.DateField()
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name="coach")
    coach_image = models.ImageField(upload_to="coachs_images/", blank=True)

    def __str__(self):
        return self.coach_name


class Player(models.Model):
    playerid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    nationality = models.ForeignKey(Nation, on_delete=models.CASCADE)
    dob = models.DateField()
    height = models.PositiveIntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="players_images/", blank=True)
    player_type = models.CharField(max_length=255, default="local")

    def __str__(self):
        return self.name


class Player_Stat(models.Model):
    playerstatid = models.AutoField(primary_key=True)
    numberofgoals = models.PositiveIntegerField(default=0)
    numberofassists = models.IntegerField(default=0)
    apperances = models.PositiveIntegerField(default=0)
    redcards = models.PositiveIntegerField(default=0)
    yellowcards = models.PositiveIntegerField(default=0)
    player = models.OneToOneField(
        Player, on_delete=models.CASCADE, related_name="player_stat"
    )

    def __str__(self):
        return self.numberofgoals


def create_player_stat(sender, instance, created, **kwargs):
    if created:
        Player_Stat.objects.create(player=instance)


post_save.connect(create_player_stat, sender=Player)


class Tournament(models.Model):
    tournamentid = models.AutoField(primary_key=True)
    totalprizepool = models.PositiveIntegerField()
    sponsor = models.ManyToManyField(Sponsor)

    def __str__(self):
        return self.totalprizepool


class Fan(models.Model):
    fanid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    nationality = models.ForeignKey(Nation, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    dob = models.DateField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Round(models.Model):
    roundid = models.AutoField(primary_key=True)
    round_name = models.CharField(max_length=100)

    def __str__(self):
        return self.round_name


class Status(models.Model):
    statusid = models.AutoField(primary_key=True)
    statusname = models.CharField(max_length=100)

    def __str__(self):
        return self.statusname


class Fixture(models.Model):
    fixtureid = models.AutoField(primary_key=True)
    round_name = models.ForeignKey(
        Round, on_delete=models.CASCADE, related_name="roundname"
    )
    time = models.DateTimeField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.time


class Result(models.Model):
    resultid = models.AutoField(primary_key=True)
    team1pts = models.PositiveIntegerField()
    team2pts = models.PositiveIntegerField()
    goal_events = models.ManyToManyField(
        Player,
        through="GoalEvent",
        through_fields=("result", "player"),
        related_name="goal_events",
    )
    fixture = models.OneToOneField(
        Fixture, on_delete=models.CASCADE, related_name="result"
    )

    def __str__(self):
        return f"Result: Team1 - {self.team1pts} points, Team2 - {self.team2pts} points"

    def update_team_scores(self, winpts, drawpts, losepts):
        if self.team1pts > self.team2pts:
            self.fixture.team1.team_stat.wins += 1
            self.fixture.team2.team_stat.loses += 1
            self.fixture.team1.team_stat.pts += winpts
            self.fixture.team2.team_stat.pts += losepts
        elif self.team1pts < self.team2pts:
            self.fixture.team1.team_stat.loses += 1
            self.fixture.team2.team_stat.wins += 1
            self.fixture.team2.team_stat.pts += winpts
            self.fixture.team1.team_stat.pts += losepts
        else:
            self.fixture.team1.team_stat.draws += 1
            self.fixture.team2.team_stat.draws += 1
            self.fixture.team1.team_stat.pts += drawpts
            self.fixture.team2.team_stat.pts += drawpts
        if self.fixture.stadium != self.fixture.team1.stadium:
            self.fixture.team1.team_stat.awaygoals += self.team1pts
        if self.fixture.stadium != self.fixture.team2.stadium:
            self.fixture.team2.team_stat.awaygoals += self.team2pts
        self.fixture.team1.team_stat.goals += self.team1pts
        self.fixture.team1.team_stat.goalsconceded += self.team2pts
        self.fixture.team2.team_stat.goals += self.team2pts
        self.fixture.team2.team_stat.goalsconceded += self.team1pts
        self.fixture.team1.team_stat.goaldifference = (
            self.fixture.team1.team_stat.goals
            - self.fixture.team1.team_stat.goalsconceded
        )
        self.fixture.team2.team_stat.goaldifference = (
            self.fixture.team2.team_stat.goals
            - self.fixture.team2.team_stat.goalsconceded
        )
        self.fixture.team1.team_stat.save()
        self.fixture.team2.team_stat.save()


class GoalType(models.Model):
    typeid = models.AutoField(primary_key=True)
    typename = models.CharField(max_length=255)

    def __str__(self):
        return self.typename


class GoalEvent(models.Model):
    eventid = models.AutoField(primary_key=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="scored_goal_events"
    )
    assist_player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="assisted_goal_events"
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    goal_type = models.ForeignKey(GoalType, on_delete=models.CASCADE)
    goal_time = models.IntegerField()

    def __str__(self):
        return f"{self.player.name} - {self.goal_type} - {self.goal_time}"

    def update_player_stats(self):
        player_stat = self.player.player_stat
        player_stat.numberofgoals += 1
        player_stat.save()
        player_stat = self.assist_player.player_stat
        player_stat.numberofassists += 1
        player_stat.save()


class Regulation(models.Model):
    regulationid = models.AutoField(primary_key=True)
    minage = models.IntegerField(default=16)
    maxage = models.IntegerField(default=40)
    minplayer = models.IntegerField(default=15)
    maxplayer = models.IntegerField(default=22)
    maxforeignplayer = models.IntegerField(default=3)
    winpts = models.IntegerField(default=3)
    drawpts = models.IntegerField(default=1)
    losepts = models.IntegerField(default=0)
    scoretime = models.IntegerField(default=90)
