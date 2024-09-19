@app.route('/book_meal', methods=['GET', 'POST'])
@login_required
def book_meal():
    if request.method == 'POST':
        meal_name = request.form.get('meal_name')
        meal_date = request.form.get('meal_date')
        new_booking = MealBooking(member_id=current_user.id, meal_name=meal_name, meal_date=meal_date)
        db.session.add(new_booking)
        db.session.commit()
        flash('Meal booked successfully!')
    return render_template('book_meal.html')
