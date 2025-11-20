from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **options):
        # Clear existing data using Djongo's raw collection access to avoid ObjectId hash issues
        from django.db import connection
        db = connection.cursor().db_conn.client['octofit_db']
        db['octofit_tracker_activity'].delete_many({})
        db['octofit_tracker_workout'].delete_many({})
        db['octofit_tracker_leaderboard'].delete_many({})
        db['octofit_tracker_user'].delete_many({})
        db['octofit_tracker_team'].delete_many({})

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
        dc = Team.objects.create(name='DC', description='DC superheroes')

        # Create users
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel, is_superhero=True)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel, is_superhero=True)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc, is_superhero=True)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc, is_superhero=True)

        # Create activities
        Activity.objects.create(user=tony, type='Running', duration=30, date=timezone.now().date())
        Activity.objects.create(user=steve, type='Cycling', duration=45, date=timezone.now().date())
        Activity.objects.create(user=bruce, type='Swimming', duration=25, date=timezone.now().date())
        Activity.objects.create(user=clark, type='Flying', duration=60, date=timezone.now().date())

        # Create workouts
        w1 = Workout.objects.create(name='Pushups', description='Upper body workout')
        w2 = Workout.objects.create(name='Situps', description='Core workout')
        w1.suggested_for.set([tony, steve])
        w2.suggested_for.set([bruce, clark])

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, points=200)
        Leaderboard.objects.create(team=dc, points=180)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
