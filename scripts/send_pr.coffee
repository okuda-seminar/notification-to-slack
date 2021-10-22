module.exports = (robot) ->

  class PullRequest
    filter_reviewer: (slack_user_id, repo) ->
      {PythonShell} = require('python-shell');

      execute_path = './scripts/read_pr.py'
      options = {
          args:[
              '-param1', slack_user_id
              '-param2', repo
          ]
      }

      pyshell = new PythonShell(execute_path, options);
      pyshell.send()
      pyshell.on('message', (pr_titles)->
        msg.send pr_titles
      )


  main = (slack_user_id, repo) ->
    pr_titles = new PullRequest().filter_reviewer(slack_user_id, repo)
    return pr_titles

  github = require("githubot")(robot)

  unless (url_api_base = process.env.HUBOT_GITHUB_API)?
    url_api_base = "https://api.github.com"

  robot.respond /showpr\s+(me\s+)?(.*)\s+pulls(\s+with\s+)?(.*)?/i, (msg)->
    repo = github.qualified_repo msg.match[2]
    slack_user_id = msg.message.user.id;
    main(slack_user_id, repo)