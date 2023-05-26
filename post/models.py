from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.conf import settings
from faker import Faker
from django.contrib.auth.models import User


class Yayinevi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.CharField(max_length=50, blank=True, null=True)
    kisa_ad = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.ad


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=2, verbose_name="Başlık")
    content = RichTextField(verbose_name="İçerik", null=True, blank=True)
    publishing_date = models.DateField(verbose_name="Yayımlanma Tarihi", auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False)
    yayin = models.ForeignKey(Yayinevi, on_delete=models.CASCADE, null=True, blank=True)
    onay = models.BooleanField(default=False, verbose_name="Onayla")

    def __str__(self):
        return self.title

    @classmethod
    def generate_fake_data(cls, count):
        fake = Faker()
        for _ in range(count):
            cls.objects.create(
                user_id=1,
                title=fake.name(),
                content=fake.text(),

            )

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"slug": self.slug})
        # return "/post/{}".format(self.id)

    def get_create_url(self):
        return reverse("post:create", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("post:update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("post:delete", kwargs={"slug": self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title.replace("ı", "i"))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-publishing_date", "id"]


class Comment(models.Model):
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=200, verbose_name="Ad Soyad")
    content = models.TextField(verbose_name="Yorum")
    created_date = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.name


class Notification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateField(auto_now_add=True)
    read = models.BooleanField(default=False)













class Gazeteci(models.Model):
    isim = models.CharField(max_length=120)
    soyisim = models.CharField(max_length=120)
    biyografi = models.TextField(blank=True, null=True)


    def __str__(self):
        return f'{self.isim} {self.soyisim}'







class Makale(models.Model):
    yazar = models.ForeignKey(Gazeteci, on_delete=models.CASCADE, related_name='makaleler')
    baslik = models.CharField(max_length=120)
    aciklama = models.CharField(max_length=200)
    metin = models.TextField()
    sehir = models.CharField(max_length=120)
    yayimlanma_tarihi = models.DateField()
    aktif = models.BooleanField(default=True)
    yaratilma_tarihi = models.DateTimeField(auto_now=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.baslik




