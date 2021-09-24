module.exports = (robot) ->
  robot.respond /my github name (.*)/i, (msg)->	
    slack_user = msg.message.user.id;
    github_user = msg.match[1]

    {PythonShell} = require('python-shell');

    execute_path = './scripts/register_username.py'
    options = {
      args:[
        '-param1', slack_user
        '-param2', github_user
      ]
    };

    pyshell = new PythonShell(execute_path, options);
    pyshell.send()
    pyshell.on('message', (message)->
      msg.send message
    );