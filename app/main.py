import os
from GPTJ.gptj_api import Completion
from flask import render_template, flash, redirect, url_for, Flask
from forms import LoginForm

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
   form = LoginForm()
   if form.validate_on_submit():
     context = "This is a therapist bot that will reframe negative thoughts in a more positive, hopeful way"
     examples = {
          "Negative: this will never work out" : "Positive: I'm having trouble right now, but it's not a big deal if this doesn't work out.",
          "Negative: My life is just filled with problems" : "Positive: I'm having some trouble right now, but I'm making plans to solve those problems.",
          "Negative: why do I suck at this" : "Positive: I have learned a lot about this topic. I want to keep learning more about it so I'll keep up the effort.",
          "Negative: why do I suck at this" : "Positive: I know what I need to improve."
     }
     context_setting = Completion(context, examples)
     prompt = form.thought.data
     User = "Patient"
     Bot = "Psychoherapist"
     max_tokens = 60
     temperature = 0.89
     top_probability = 1.0

     response = context_setting.completion(prompt,
              user=User,
              bot=Bot,
              max_tokens=max_tokens,
              temperature=temperature,
              top_p=top_probability)

     flash(response)
     
   return render_template('index.html',  title='Input Form', form=form)

if __name__ == "__main__":
  app.run(debug=False, host = '0.0.0.0')

