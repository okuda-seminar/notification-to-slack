module.exports = (robot) ->

  github = require("githubot")(robot)
  CronJob = require('cron').CronJob
  JapaneseHolidays = require('japanese-holidays')

  unless (url_api_base = process.env.HUBOT_GITHUB_API)?
    url_api_base = "https://api.github.com"

  job = new CronJob '0 12 16 * * 1-5', () ->
    today = new Date();
    holiday = JapaneseHolidays.isHoliday(today);
    if holiday 
      console.log("今日は " + holiday + " です")
    else
      console.log("aaaa")
  job.start()

  robot.respond /showprr\s+(me\s+)?(.*)\s+pulls(\s+with\s+)?(.*)?/i, (msg)->
    username = msg.message.user.id;
    console.log(username)


    {PythonShell} = require('python-shell');

    options = {
      pythonPath: '/opt/anaconda3/bin/python',
      pythonOptions: ['-u'], 
      scriptPath: './'
    };
    
    pyshell = new PythonShell('./scripts/sqlite_read.py',options);
    # sends a message to the Python script via stdin
    pyshell.send(username);
    pyshell.on('message', (message)-> 
      # received a message sent from the Python script (a simple "print" statement)
      user_name = message

      repo = github.qualified_repo msg.match[2]
      filter_reg_exp = new RegExp(msg.match[4], "i") if msg.match[3]
      summary = ""

      github.get "#{url_api_base}/repos/#{repo}/pulls", (pulls) ->
        if pulls.length == 0
          summary = "Achievement unlocked: open pull requests zero!"
        else
          for pull in pulls
            for reviewer in pull.requested_reviewers
              if "#{reviewer.login}" == user_name
                summary = summary + "\n\t#{pull.title} - #{pull.user.login}: #{pull.html_url}"
              
        msg.send summary
    );
