> EVENTIA

1. Eventia is a web-based event scheduling application for colleges. This is a Django framework-based web application.

> OVERVIEW

* The main goal of this application is to make the process of managing each event as simple as possible by providing a web interface for the event organiser, event manager, and participants.
* Eventia can manage different user groups and their permission.
* The event organiser can schedule and organise events, while the event manager can only oversee the events to which they have been allocated.
* Participants will sign up for his account using an email address that will be checked using an OTP authentication mechanism.

> EVENT PARTICIPANT USER GROUP

The participants have access to the following functionalities.

1. Event participants can register, reset password, and access a home page which the admin user can configure.
2. Participants can change their password by entering their old password and new password.
3. Event participants gets an email to confirm their account after registering, or after sending request to reset password.
4. Dashboard - The participant dashboard displays a list of the events in which they participated, as well as information such as the event's name, place, date, and time.
5. The position will be shown in the dashboard if they have been selected for the next level or if they have won.
6. The profile page contains all of their information that they entered during registration which can be updated by them, events participated, and the date and time of those events. They will register for new events by updating the list of events in their profile tab.
7. Participants may form their own teams or join existing ones. (A participant should only be a member of one team at a time for an event.)
8. To join or create a team, the name of the team and the event should be provided.

> ADMIN USER GROUP

There are different groups of admin users to manage the event and each group has their own set of tasks they can perform.

> Superuser

* The superuser is in-charge of creating groups as event organizers and event managers, and has all access to the system.
* The superuser can add or remove groups, events, teams, and winners, as well as send messages to other users.
* These are the tasks that will be divided and distributed to the other two user groups for managing the event.
* They can track the history and also the recent actions made.

> Event Organizer

* The event organizer takes control of all the events.
* They have the access to add or remove activities, notifications, users, and winners.
* They can only change teams, and cannot create a new team.
* They can track the history and also the recent actions made.

> Event Manager

* Event manager is responsible for maintaining a single event under their control.
* They can change the details about their event, add or remove winners.
* Just has view access to the message and user information.
