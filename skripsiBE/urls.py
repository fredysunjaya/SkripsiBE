"""
URL configuration for SecureVoteBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from skripsiBE.app.views import users
from skripsiBE.app.views import votings
from skripsiBE.app.views import voting_participants
from skripsiBE.app.views import voting_choices
from skripsiBE.app.views import voting_candidates

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('users/', users.users_list),
    path('users/<int:id>/', users.user_details),

    path('votings/', votings.votings_list),
    path('votings/<int:id>/', votings.voting_details),

    path('participants/', voting_participants.voting_participants_list),
    path('participants/<int:id>/', voting_participants.voting_participant_details),

    path('choices/', voting_choices.voting_choices_list),
    path('choices/<int:pk>/', voting_choices.voting_choice_details),

    path('candidates/', voting_candidates.voting_candidates_list),
    path('candidates/<int:pk>', voting_candidates.voting_candidate_details),
]
