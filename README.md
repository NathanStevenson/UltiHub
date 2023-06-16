# UltiHub
Premier Ultimate Frisbee Management Portal built using Django, hosted by Vercel, and UI developed using Figma.

#### Want to Contribute:
Feel free to fork the repository and creating pull requests. Can be anything from code or ideas in the "Features" section below.

## Important Links
* Website URL: __blank__
* Figma Design: https://www.figma.com/file/WfzGyg4ZP3vmL1oQzRNcdo/UltiHub-Designs?type=design&node-id=0-1&t=BddygqAfsEESea1W-0
* PostGresSQL Database: __blank__

### Future Plans
- [x] Design the UI using Figma.

- [ ] Host a default Django app on Vercel with hot reloading

- [ ] Figure out how to datascrape USAU (namely how to convert the teamIDs into usuable team names)

- [ ] Begin coding the project. Stages described below:
    - Code the default landing page (has our logo and asks you to search for your team)
    - Code the process of adding a new team via a form. Necessary stuff (team name, point of contacts email, team password, team logo)
    - Code the default landing home page for the team
    - Users can customize their profile (show what teams they have played for in the past, favorite workout, favorite frisbee throw, profile photo)
    - Include the settings menu can click on their profile photo (if admin can add new stuff to team landing page, else edit profile, contact page, about us page)
    - Implement each of the above features and UI described and allow teams to customize their default landing page
    - Use Night Train guys to help test and see if they have any feedback about what to add

- [ ] After thorough testing release to the public (if really flushed out look into payment gate services ($10 a year))

- [ ] Develop an app for the plaform

### Features

#### Suggestions

#### Permissions/Logistics
* Whoever added your team to the database will be the original admin for your team
* Upon adding your team we will check it is a team and ask you to verify by sending you an email
* Each team can have up to 3 admin, these individuals will be able to assign roles (captain, coach, player) to other team members,
as well as remove/assign admin to others.
* Specific features will only be available to admin/captains/coaches: customizing your teams portal, adding upcoming events, adding practice plans, editing team logistics.
* Users will be forced to sign in via Google Login before joining a team

#### Landing Page
* Landing Page where you can search for your team or add your team to our database
* Add new team form where you can upload your teams email as well as provide information about your team and your contact email
* When adding a new portal you will specify a password which you can share with your team to keep teams separate

#### Team Home Page
* After joining your team's portal this will be your teams home page and will provide many different features
* Features provided on the home page by default will be: Upcoming Events, Team Logistics/Practice-Plans, Playbook, Roster, Personal Profile Dropdown
* Users with elevated privileges can choose to also enable film review amd team discussion board tabs to be added to the Team Logistics Page
* These users can also add a tab called workouts to playbook where teammates can share new workouts they have found
* The default home page will include some basic information about your team as well as the important upcoming events

#### User Profile
* Users can upload their own personal profile picture to the site as well as include some personal information
* Users can also add some fun facts about themselves and frisbee
* By default our program will look up each player's history via USAU for team history (players can add teams they practiced with)

#### Team Logistics
* By default this will have numerous tabs you can toggle between
* The default tab will be the practice plans for that day or the upcoming practice
* Users with elevated privileges will also be able to edit a different tab which includes stuff such as carpools for tournaments, 
hotel+field addresses, what field/time next practice is, as well as an ongoing transparent team costs, dues, and payments

* Users with elevated privileges can also enable two other tabs to appear here: film room and discussion board
* Discussion board will allow all users to post questions they have and facilitate discussion
* Film Room will allow teams to link their film or other teams film and the portal will add some nice icons and make it look clean. In upload film form have boxes for URL, names of teams, and season.

#### Players
* This will include a list of all members of the current roster and the coaches. You will be able to examine all other players profiles.

#### Playbook
* In the beginning this will allow teams to link their Ultiplays account to their portal with future plans to expand to allow users to
add plays directly on the portal
* Admins can also enable the workouts tab in this menu option which will allow players to post any workout they have done that
they believe will benefit the team.

#### Profile Dropdown Menu
* In this menu users will be able to view their profile and admins will be able to customize their teams portal page, and grant user privileges
* In this menu will also contain links to our contact page (nts7bcj@virginia.edu) and an About Us page where I describe why I built this website/who I am.

#### Fun Extras
* Implement a "Stalled Out" custom 404 page
