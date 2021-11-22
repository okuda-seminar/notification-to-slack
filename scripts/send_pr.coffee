module.exports = (robot) ->
  robot.respond /showpr\s+(me\s+)?(.*)\s+pulls(\s+with\s+)?(.*)?/i, (msg)->
    github = require("githubot")(robot)

    unless (url_api_base = process.env.HUBOT_GITHUB_API)?
      url_api_base = "https://api.github.com"

    slack_user_id = msg.message.user.id;
    repo = github.qualified_repo msg.match[2]

    {PythonShell} = require('python-shell');

    execute_path = './scripts/read_pr.py'
    options = {
      args:[
        '-param1', slack_user_id
        '-param2', repo
      ]
    };

    pyshell = new PythonShell(execute_path, options);
    pyshell.send()
    pyshell.on('message', (message)->
      msg.send message
    );