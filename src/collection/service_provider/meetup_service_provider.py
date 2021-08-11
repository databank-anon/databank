import sys

sys.path.append('.')

from databank.application import Application
from databank.memory import Cell
import base64
from pathlib import Path

app = Application(None, None, 2, "Meetup", "127.0.0.1", None, "The answer is no", databank_side=False)

img_base64 = base64.b64encode(open("collection/service_provider/banner.png", "rb").read()).decode('utf-8')

my_ad = f"""<img class="card-img-top" src="data:image/png;base64,{img_base64}">
          <div class="card-body">
             <h5 class="card-title">Get emacs!</h5>
             <h6 class="card-subtitle mb-2 text-muted">Advertisement</h6> 
             <p class="card-text">Emacs is the best text editor ever, way better than Vi</p>
             <a href="https://gnu.org/software/emacs" class="btn btn-primary">To website</a>
          </div>"""

@app.callback('/ad')
def ad():
    return Cell(my_ad)

app.server.start()


