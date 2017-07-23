# **randi**

## Description

randi is a discord bot posting xkcd comic. Using an in-house index created from
the transcript of the comics, the bot answer to users' queries with a relevant
comic.

## Table of content

* [Installation](https://github.com/nhatzHK/randi#Installation)
* [Usage](https://github.com/nhatzHK/randi#Usage)
* [Contributing](https://github.com/nhatzHK/randi#Contributing)
  * [Beginner issues](https://github.com/nhatzHK/randi#Beginner))

## Installation

* Clone the repo: `git clone https://github.com/nhatzHK/randi`
* Install dependencies: (**N.B.**: Tested only with python 3)
  `pip install discord.py`or `pip3 install discord.py` depending on your
  platform.
* Modify configuration files
  `cd randi`
  * xkcd.config.json
  ```sh
  cd json
  cp xkcd.config.json xkcd.config.priv
  # Modify the new file to add the appropriate information
  ```
  * xkcd.path.json
  ```sh
  cd ../python/client
  cp xkcd.path.json xkcd.path.json.priv
  # Modify the new file to add the appropriate information
  ```

## Usage

Make sure the bot is in a server before this step. See
[here](https://github.com/nhatzHK/randi/wiki#bot-devs) for how to add the bot to
a server.

Once the bot is created and add in a server, run it:
`python xkcd.py xkcd.path.json.priv`

To use the bot from discord, use the help command (`<prefix>help`) to see the commands avvailable and how to use them.

For more detailed usage see
[here](https://github.com/nhatzHK/randi/wiki#how-to))

## Contributing

randi is Open Source. You can clone it, fork it, copy it and of course se it freely and in any way you want that doesn't infringe the [license](https://github.com/nhatzHK/randi/blob/master/License). 

You can contribute to randi by taking one of the current issues and solving it or creating an issue yourself. You can also join the [development server](https://discord.gg/rwjq3Mh). You can help. It does not matter if you know programming or not. You can help. Visit the issue list, the project list and the milestine list to find out where the bot's development is headed.

### Beginner

If you're a beginner programmer looking to start contributing on a ez-pz project
the [up-for-grabs](https://github.com/nhatzHK/randi/labels/up-for-grabs) issues
are for you. Pick one and try to solve it, if you stumble on errors, aka
problems, join the server or seek for help in the comment section of the issue.
