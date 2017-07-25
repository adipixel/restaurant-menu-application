from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # restaurant = session.query(Restaurant).first()
    # items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    # output = ''
    # for i in items:
    #     output += i.name
    #     output += '</br>'
    #     output += i.price
    #     output += '</br>'
    #     output += i.description
    #     output += '</br>'
    #     output += '</br>'

    return "List of all Restaurants"

@app.route('/restaurant/new/')
def newRestaurant():
    return "Create new Restaurant"


@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return "Edit restaurant %s" %restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return "Delete restaurant %s" %restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
    # restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    # return render_template('menu.html', restaurant = restaurant, items = items)
    return "Menu for the restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        # newItem = MenuItem(name=request.form['name'], description=request.form[
        #                    'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        # session.add(newItem)
        # session.commit()
        # flash("New menu item created!")
        # return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        return "POST for creating menu item of restaurant %s" %restaurant_id 
    else:
        # return render_template('newmenuitem.html', restaurant_id=restaurant_id)
        return "GET - form for creating new menu item"


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
#    editedItem = session.query(MenuItem).filter_by(id=MenuID).one()
    if request.method == 'POST':
        # if request.form['name']:
        #     editedItem.name = request.form['name']
        # session.add(editedItem)
        # session.commit()
        # flash("Item updated!")
        # return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
        return "POST for editing menu item of restaurant %s" %restaurant_id
    else:
        #return render_template('editmenuitem.html', restaurant_id=restaurant_id, MenuID=MenuID, item=editedItem)
        return "GET - form for editing menu item"


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	# item = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		# session.delete(item)
		# session.commit()
		# flash("Item Deleted!")
		# return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
            return "POST for deleting menu item from restaurant %s" %restaurant_id
	else:
		# return render_template('deletemenuitem.html', item = item, restaurant_id = restaurant_id)
            return "GET - alert for deleting menu item"

# @app.route('/restaurants/<int:restaurant_id>/menu/json')
# def retaurantMenuJson(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
#     return jsonify(MenuItems= [i.serialize for i in items])

# @app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
# def retaurantMenuItemJson(restaurant_id, menu_id):
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     item = session.query(MenuItem).filter_by(id=menu_id).one()
#     return jsonify(MenuItems= item.serialize)


if __name__ == '__main__':
	app.secret_key = "my_secret_key"
	app.debug = True
	app.run(host='0.0.0.0', port=5000)