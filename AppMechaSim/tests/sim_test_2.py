import sim_test

# Print the initial value
print("Before:", sim_test.sim_start_button_pushed)

# Update the variable using the function
sim_test.update_variable()

# Print the updated value
print("After:", sim_test.sim_start_button_pushed)