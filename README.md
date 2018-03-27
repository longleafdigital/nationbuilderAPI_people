# Nationbuilder API People App (nationbuilderAPI_people) #
Using the NB API to edit people entities for Developer certification: https://nationbuilder.com/developer_exercises

This app is built with Python on Flask. It should serve the purpose of creating, editing, and deleting people from a Nation's database via the API as specificed in the exercises document.

Launching the app from it's root file "/" will begin the authentication for the default nation "blakemizelledev" (my sandbox). This is just for demo purposes. If you wish to access another nation with this code, click "Or Change Slug" on the index page. This starts the authorzation / authentication of the app for any nation given it's slug (and of course, administrator privileges).

After using the "Authenticate" button for the nation of your choosing, you can interact with any of the following menu options:

- People Count
- People List
- People Create
- People Update
- People Delete

## Functions Roadmap ##
The following is my walkthrough roadmap of the app functions:

- "/" (index)
  - "/authenticate"
   - "/people/count"
   - "/people/list"
   - "/people/create"
   - "/people/update"
   - "/people/delete"
