from flask import Flask
import main


app=Flask(__name__)


@app.route('/')
def index():
    data=main.get_reviews('https://www.amazon.in/product-reviews/B077BFH786/&reviewerType=all_reviews/ref=cm_cr_arp_d_viewpnt_rgt?filterByStar=critical&pageNumber=1')
    return str(data)


if __name__=='__main__':
    app.run(debug=True)