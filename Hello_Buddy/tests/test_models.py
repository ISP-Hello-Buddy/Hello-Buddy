from django.test import TestCase
from django.urls import reverse
from Hello_Buddy.models import Event, HostOfEvent, ParticipantOfEvent, Profile
from django.contrib.auth.models import User
import datetime


class BaseSet(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username='breeze',
            password='bb123456',
            email='b@mail.com',
        )

        self.user2 = User.objects.create(
            username='breeze2',
            password='bb123456',
            email='b2@mail.com',
        )

        self.event1 = Event.objects.create(
            name='Football',
            place='Kaset',
            participant=10,
            date='2022-11-27',
            time='20:00:00',
        )

        self.event2 = Event.objects.create(
            name='Badminton',
            place='Kaset',
            participant=10,
            joined=10,
            date='2022-11-27',
            time='21:00:00',
        )
        return super().setUp()


class EventModelTest(BaseSet):

    def test_null_field(self):
        """ to test null field of the event"""
        self.assertEqual(self.event1.joined, 0)
        self.assertEqual(self.event1.image_upload, 'event/images/default.jpg')
        self.assertEqual(self.event1.type, None)

    def test_full_event(self):
        """ to test that event is already full"""
        self.assertTrue(self.event2.full())

    def test_is_active_event(self):
        """ to test if not yet time of event. it will return true"""
        event = Event.objects.create(
            name='Badminton',
            place='Kaset',
            participant=10,
            joined=10,
            date=(datetime.datetime.today() +
                  datetime.timedelta(days=1)).date(),
            time=datetime.datetime.today().time(),
        )

        event2 = Event.objects.create(
            name='Badminton',
            place='Kaset',
            participant=10,
            joined=10,
            date=datetime.datetime.today().date(),
            time=(datetime.datetime.today() +
                  datetime.timedelta(hours=1)).time(),
        )

        self.assertTrue(event.is_active())
        self.assertTrue(event2.is_active())

    def test_is_not_active_event(self):
        """ to test if datetime of event is past. it will return false"""
        event = Event.objects.create(
            name='Badminton',
            place='Kaset',
            participant=10,
            date=(datetime.datetime.today() -
                  datetime.timedelta(days=1)).date(),
            time=datetime.datetime.today().time(),
        )

        event2 = Event.objects.create(
            name='Badminton',
            place='Kaset',
            participant=10,
            date=(datetime.datetime.today() -
                  datetime.timedelta(days=1)).date(),
            time=(datetime.datetime.today() -
                  datetime.timedelta(hours=1)).time(),
        )

        self.assertFalse(event.is_active())
        self.assertFalse(event2.is_active())


class HostOfeventModelTest(BaseSet):

    def test_host_and_event_that_created(self):
        """ Test host of event and event that created"""
        host = HostOfEvent.objects.create(
            user=self.user1,
            event=self.event1
        )

        self.assertEqual(host.user.username, 'breeze')
        self.assertEqual(host.event.name, 'Football')

    def test_many_event_same_user(self):
        """ Users allow to create manay event"""
        host1 = HostOfEvent.objects.create(
            user=self.user1,
            event=self.event1
        )

        host2 = HostOfEvent.objects.create(
            user=self.user1,
            event=self.event2
        )

        self.assertEqual(len(HostOfEvent.objects.all()), 2)
        self.assertEqual(host1.user.username, 'breeze')
        self.assertEqual(host1.event.name, 'Football')
        self.assertEqual(host2.user.username, 'breeze')
        self.assertEqual(host2.event.name, 'Badminton')

    def test_delete_event(self):
        """ Test if user delete event. it will delete all that event connect"""
        HostOfEvent.objects.create(
            user=self.user1,
            event=self.event1
        )
        # test before delete
        self.assertEqual(len(HostOfEvent.objects.all()), 1)
        self.event1.delete()
        # test after delete
        self.assertEqual(len(HostOfEvent.objects.all()), 0)

    def test_delete_user(self):
        """ Test if user delete their own user. it will delete all that user connect"""
        HostOfEvent.objects.create(
            user=self.user2,
            event=self.event2
        )
        # test before delete
        self.assertEqual(len(HostOfEvent.objects.all()), 1)
        self.user2.delete()
        # test after delete
        self.assertEqual(len(HostOfEvent.objects.all()), 0)


class ParticipantOfEventModelTest(BaseSet):

    def test_user_and_event_that_joined(self):
        """ Test user that joined the event """
        par = ParticipantOfEvent.objects.create(
            user=self.user1,
            event=self.event1
        )

        self.assertEqual(par.user.username, 'breeze')
        self.assertEqual(par.event.name, 'Football')

    def test_user_join_many_event(self):
        """ Users allow to join manay event"""
        par1 = ParticipantOfEvent.objects.create(
            user=self.user1,
            event=self.event1
        )

        par2 = ParticipantOfEvent.objects.create(
            user=self.user1,
            event=self.event2
        )

        self.assertEqual(len(ParticipantOfEvent.objects.all()), 2)
        self.assertEqual(par1.user.username, 'breeze')
        self.assertEqual(par1.event.name, 'Football')
        self.assertEqual(par2.user.username, 'breeze')
        self.assertEqual(par2.event.name, 'Badminton')

    def test_users_join_same_event(self):
        """ Different users join the same event"""
        par1 = ParticipantOfEvent.objects.create(
            user=self.user1,
            event=self.event1
        )

        par2 = ParticipantOfEvent.objects.create(
            user=self.user2,
            event=self.event1
        )

        self.assertEqual(len(ParticipantOfEvent.objects.all()), 2)
        self.assertEqual(par1.user.username, 'breeze')
        self.assertEqual(par1.event.name, 'Football')
        self.assertEqual(par2.user.username, 'breeze2')
        self.assertEqual(par2.event.name, 'Football')

    def test_delete_event(self):
        """ Test if user delete event. it will delete all that event connect"""
        ParticipantOfEvent.objects.create(
            user=self.user1,
            event=self.event1
        )
        ParticipantOfEvent.objects.create(
            user=self.user2,
            event=self.event1
        )
        # test before delete
        self.assertEqual(len(ParticipantOfEvent.objects.all()), 2)
        self.event1.delete()
        # test after delete
        self.assertEqual(len(ParticipantOfEvent.objects.all()), 0)

    def test_delete_user(self):
        """ Test if user delete their own user. it will delete all that user connect"""
        ParticipantOfEvent.objects.create(
            user=self.user2,
            event=self.event2
        )
        ParticipantOfEvent.objects.create(
            user=self.user2,
            event=self.event1
        )
        # test before delete
        self.assertEqual(len(ParticipantOfEvent.objects.all()), 2)
        self.user2.delete()
        # test after delete
        self.assertEqual(len(ParticipantOfEvent.objects.all()), 0)


class ProfileModelTest(BaseSet):

    def test_create_user_profie(self):
        """ test create user profile"""
        # Auto create profile when user is created
        user = Profile.objects.filter(id=1).first()
        self.assertEqual(user.user.username, 'breeze')
        self.assertEqual(user.avatar, "profile/images/default.jpg")
        self.assertEqual(user.bio, '...')

    def test_delete_user(self):
        """ test delete user"""

        self.assertEqual(len(Profile.objects.all()), 2)
        self.user1.delete()
        self.assertEqual(len(Profile.objects.all()), 1)
        self.user2.delete()
        self.assertEqual(len(Profile.objects.all()), 0)
