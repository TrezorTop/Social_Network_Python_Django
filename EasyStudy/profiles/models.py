from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.template.defaultfilters import slugify

from .utils import get_random_code


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        query_set = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        # print(query_set)
        # print("------------")

        accepted = set([])
        for relation in query_set:
            if relation.status == 'accepted':
                accepted.add(relation.receiver)
                accepted.add(relation.sender)
        # print(accepted)
        # print("------------")

        available = [profile for profile in profiles if profile not in accepted]
        # print(available)
        # print("------------")
        return available

    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(default="no bio...", max_length=300)
    email = models.EmailField(max_length=300, blank=True)
    contacts = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    subscriptions = models.ManyToManyField("profiles.Profile", blank=True)
    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username} - profile"

    def get_absolute_url(self):
        return reverse("profiles:profile_detail_view", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

    def get_subscriptions(self):
        return self.subscriptions.all()

    def get_friends_no(self):
        return self.friends.all().count()

    def get_posts_no(self):
        return self.posts.all().count()

    def get_all_author_posts(self):
        return self.posts.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

    def get_likes_received_no(self):
        posts = self.posts.all()
        total_liked = 0
        for item in posts:
            total_liked += item.liked.all().count()
        return total_liked

    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.slug = slugify(str(self.user.username))

        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name
        self.__initial_username = self.user.username

    def save(self, *args, **kwargs):
        slug_exists = False
        to_slug = self.slug

        to_slug.replace('.', '')
        if self.user.username != self.__initial_username or self.slug == "":
            if self.user.username:
                to_slug = slugify(str(self.user.username))
                slug_exists = Profile.objects.filter(slug=to_slug).exists()
                while slug_exists:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    slug_exists = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user.username)
        self.slug = to_slug
        super().save(*args, **kwargs)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted')
)


class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        query_set = Relationship.objects.filter(receiver=receiver, status='send')
        return query_set


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender} - {self.receiver} - {self.status}"
