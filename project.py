from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
# #Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}



@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new/', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method =='POST':
		restaurant = Restaurant(name = request.form['name'])
		session.add(restaurant)
		session.commit()
		flash('New restaurant %s created!' % restaurant.name)
		return redirect(url_for('showRestaurants'))

	else:
		return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		restaurant.name = request.form['name']
		session.add(restaurant)
		session.commit()
		flash("Restaurant name updated.")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurant)
		session.commit()
		flash("Restaurant deleted.")
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		item = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(item)
		session.commit()
		flash("New menu item created!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',
		   methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id = restaurant.id).one()
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name']
		session.add(item)
		session.commit()
		flash("Item updated!")
		return redirect(url_for('showMenu', restaurant_id = restaurant.id))
	else:
		return render_template('editMenuItem.html', restaurant = restaurant, item = item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	item = session.query(MenuItem).filter_by(id = menu_id, restaurant_id = restaurant.id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		flash("Item Deleted!")
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', item = item, restaurant = restaurant)

@app.route('/restaurants/json')
def retaurantsJson():
    restaurant = session.query(Restaurant).all()
    return jsonify(MenuItems= [r.serialize for r in restaurant])

@app.route('/restaurant/<int:restaurant_id>/menu/json')
def retaurantMenuJson(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems= [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json')
def retaurantMenuItemJson(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItems= item.serialize)


if __name__ == '__main__':
	app.secret_key = "my_secret_key"
	app.debug = True
	app.run(host='0.0.0.0', port=5000)