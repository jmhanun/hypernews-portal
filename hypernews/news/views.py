from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.views.generic.base import View
from django.conf import settings 

import json

import datetime, random

# path_json = f"../{settings.NEWS_JSON_PATH}"
path_json = f"{settings.NEWS_JSON_PATH}"


class Greetings(View):
    def get(self, request, *args, **kwargs):
        # return HttpResponse("<h1>Coming soon</h1><a href='/news/'> Check the news</a>")
        return redirect("/news/")


class Posting(View):
    def get(self, request, post_link, *args, **kwargs):
        with open(path_json) as f_json:
                posts = json.load(f_json)
        context = {}
        for post in posts:
            if post["link"] == post_link:
                context["post"] = post
                break

        return render(request, "news/post.html", context=context)


class News(View):
    def get(self, request, *args, **kwargs):
        with open(path_json) as f_json:
                posts = json.load(f_json)
        
        all_news = []
        q = ""
        if "q" in request.GET:
            q = request.GET['q']

        for post in posts:
            if q in post["title"]:
                post["fecha"] = post["created"][:10]
                all_news.append(post)


        dates = set()
        for post in all_news:
            date = post["created"][:10]
            dates.add(date)

        context = {
            "all_news": all_news,
            "order": sorted(dates, reverse=True),
        }
        return render(request, "news/index.html", context=context)


class Create(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/new.html")

    def post(self, request, *args, **kwargs):
        with open(path_json) as f_json:
                posts = json.load(f_json)

        link = random.randint(1,99999)
        links = [d['link'] for d in posts]

        while link in links:
            print("repe",link)
            link = random.randint(1,99999)
        
        new_new = {
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "text": request.POST['text'], 
            "title": request.POST['title'], 
            "link": link
        }

        posts.append(new_new)

        with open(path_json, "w") as f_json:
            json.dump(posts, f_json)


        
        return redirect("/news/")
