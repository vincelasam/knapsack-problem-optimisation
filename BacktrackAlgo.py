import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import scrolledtext

# Global variables to store the best solution
best_items = []
best_importance = 0

def backtrack(items, prices, importance, index, budget, current_items, current_importance):
    
    global best_items, best_importance #Declare global variables
    
    # Notify dev that program is running
    if index == 0:
        print(f"Starting backtrack with budget: {budget}, items: {len(items)}")
    
    # Base case: checked all items
    if index == len(items):
        if current_importance > best_importance:
            best_importance = current_importance  
            best_items = current_items.copy()
            print(f"New best found: {best_items} with importance {best_importance}")
        return
    
    # Get current item info
    item_name = items[index]
    item_price = prices[index] 
    item_importance = importance[index]
    
    # Choice 1: Include this item (if affordable)
    if item_price <= budget:
        current_items.append(item_name)
        backtrack(items, prices, importance, index + 1, 
                 budget - item_price, current_items, 
                 current_importance + item_importance)
        current_items.pop()  # Backtrack
    
    # Choice 2: Skip this item  
    backtrack(items, prices, importance, index + 1, 
             budget, current_items, current_importance)
    

class KnapsackGUI:

    # App Interface


    def __init__(self, root):
        #Constructor/ Initialization for GUI
        self.root = root
        self.root.title("Knapsack Problem Solver")
        self.root.geometry("650x750")
        self.root.resizable(False, False)  
        self.root.configure(bg="#0F172A")  
        
        self.items = []
        self.prices = []
        self.importance = []
        self.budget_set = False  # Track if budget has been set
        self.current_budget = 0.0  # Store the current budget value
        
        self.create_widgets()
    
    
    def create_widgets(self):
        # Title 
        title = tk.Label(self.root, text="Knapsack Problem Solver", 
                        font=('Times New Roman', 20, 'bold'), bg='#0F172A', fg='#F9FAFB')
        title.pack(pady=15)
        
        # Budget input frame
        budget_frame = tk.Frame(self.root, bg='#0F172A', relief='raised', bd=2)
        budget_frame.pack(pady=10, padx=20)
        
        tk.Label(budget_frame, text="Budget: ", font=('Times New Roman', 14, 'bold'), 
                bg='#14B8A6', fg='#F9FAFB').pack(side='left', padx=10, pady=10)
        
        self.budget_entry = tk.Entry(budget_frame, font=('Times New Roman', 14), width=15,
                                    bg='#E6FFFA', fg='#065F46', insertbackground='#065F46')
        self.budget_entry.pack(side='left', padx=10, pady=10)
        
        # Set Budget button
        self.set_budget_btn = tk.Button(budget_frame, text="Set Budget", command=self.set_budget,
                                       bg='#10B981', fg='#F9FAFB', font=('Times New Roman', 12, 'bold'),
                                       padx=15, pady=8, relief='raised', bd=3,
                                       activebackground='#059669', activeforeground='#F9FAFB')
        self.set_budget_btn.pack(side='left', padx=10, pady=10)
        
        # Budget status label
        self.budget_status_label = tk.Label(budget_frame, text="Enter budget and click 'Set Budget'", 
                                          font=('Times New Roman', 10), bg='#0F172A', fg="#94B5B8")
        self.budget_status_label.pack(side='left', padx=15, pady=10)
        
        # Add item frame
        add_frame = tk.LabelFrame(self.root, text="Add New Item", 
                                 font=('Times New Roman', 14, 'bold'), bg='#1E293B', 
                                 fg='#F9FAFB', padx=15, pady=15, relief='raised', bd=3)
        add_frame.pack(pady=15, padx=20, fill = 'x')
        
        # Item name
        tk.Label(add_frame, text="Item Name/Serial No. :", font=('Times New Roman', 12, 'bold'),
                bg='#1E293B', fg='#F9FAFB').grid(row=0, column=0, sticky='w', pady=8)
        self.name_entry = tk.Entry(add_frame, font=('Times New Roman', 12), width=25,
                                  bg='#E6FFFA', fg='#065F46', insertbackground='#065F46')
        self.name_entry.grid(row=0, column=1, padx=15, pady=8)
        
        # Item price
        tk.Label(add_frame, text="Price: ", font=('Times New Roman', 12, 'bold'),
                bg='#1E293B', fg='#F9FAFB').grid(row=1, column=0, sticky='w', pady=8)
        self.price_entry = tk.Entry(add_frame, font=('Times New Roman', 12), width=25,
                                   bg='#E6FFFA', fg='#065F46', insertbackground='#065F46')
        self.price_entry.grid(row=1, column=1, padx=15, pady=8)
        
        # Item importance
        tk.Label(add_frame, text="Importance (1-10):", font=('Times New Roman', 12, 'bold'),
                bg='#1E293B', fg='#F9FAFB').grid(row=2, column=0, sticky='w', pady=8)
        self.importance_entry = tk.Entry(add_frame, font=('Times New Roman', 12), width=25,
                                        bg='#E6FFFA', fg='#065F46', insertbackground='#065F46')
        self.importance_entry.grid(row=2, column=1, padx=15, pady=8)
        
        # Add item button
        add_btn = tk.Button(add_frame, text="Add Item", command=self.add_item,
                           bg='#14B8A6', fg='#F9FAFB', font=('Times New Roman', 12, 'bold'),
                           padx=25, pady=8, relief='raised', bd=3,
                           activebackground='#0F766E', activeforeground='#F9FAFB')
        add_btn.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Items list frame
        list_frame = tk.LabelFrame(self.root, text="Items in Cart", 
                                  font=('Times New Roman', 14, 'bold'), bg='#1E293B', 
                                  fg='#F9FAFB', padx=15, pady=15, relief='raised', bd=3)
        list_frame.pack(pady=15, padx=20, fill='both', expand=True)
        
        # Scrollable text widget for items list (READ-ONLY)
        self.items_text = scrolledtext.ScrolledText(list_frame, height=8, width=65,
                                                   font=('Times New Roman', 11), bg='#E6FFFA', 
                                                   fg='#065F46', insertbackground='#065F46',
                                                   state='disabled', wrap='word')
        self.items_text.pack(fill='both', expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg='#0F172A')
        buttons_frame.pack(pady=15)
        
        # Calculate button
        calc_btn = tk.Button(buttons_frame, text="Calculate Best Selection", 
                            command=self.calculate, bg='#F59E0B', fg='#F9FAFB',
                            font=('Times New Roman', 14, 'bold'), padx=25, pady=12,
                            relief='raised', bd=4, activebackground='#D97706',
                            activeforeground='#F9FAFB')
        calc_btn.pack(side='left', padx=15)
        
        # Clear button
        clear_btn = tk.Button(buttons_frame, text="Clear All", 
                             command=self.clear_all, bg='#EF4444', fg="#F9FAFB",
                             font=('Times New Roman', 14, 'bold'), padx=25, pady=12,
                             relief='raised', bd=4, activebackground='#DC2626',
                             activeforeground='#F9FAFB')
        clear_btn.pack(side='left', padx=15)
        
        # Results frame
        results_frame = tk.LabelFrame(self.root, text="Best Solution", 
                                     font=('Times New Roman', 14, 'bold'), bg='#1E293B', 
                                     fg='#F9FAFB', padx=15, pady=15, relief='raised', bd=3)
        results_frame.pack(pady=15, padx=20, fill='x')
        
        # Results text widget (READ-ONLY)
        self.results_text = scrolledtext.ScrolledText(results_frame, height=6, width=65,
                                                     font=('Times New Roman', 11), bg='#E6FFFA',
                                                     fg='#065F46', insertbackground='#065F46',
                                                     state='disabled', wrap='word')
        self.results_text.pack(fill='x')
        

        # Initialize displays
        self.update_items_display()
        self.update_results_display("Ready to calculate! Set budget and add items first.")
    
    def set_budget(self):
        #Set the budget (one-time only until cleared)
        if self.budget_set:
            messagebox.showinfo("Budget Already Set", 
                              f"Budget is already set to {self.current_budget:.2f}\n\n" +
                              "Use 'Clear All' to reset and enter a new budget.")
            return
        
        budget_str = self.budget_entry.get().strip()
        if not budget_str:
            messagebox.showerror("Missing Budget", "Please enter a budget amount!")
            return
            
        budget_valid, budget_result = self.validate_budget(budget_str)
        if not budget_valid:
            messagebox.showerror("Invalid Budget", budget_result)
            return
        
        # Set the budget
        self.current_budget = budget_result
        self.budget_set = True
        
        # Disable the budget entry and button
        self.budget_entry.config(state='disabled', bg='#F3F4F6')
        self.set_budget_btn.config(state='disabled', bg='#6B7280')
        
        # Update status label
        self.budget_status_label.config(text=f"Budget set: {self.current_budget:.2f} ✓", 
                                      fg='#94B5B8')
        
        # Show success message
        messagebox.showinfo("Budget Set", f"Budget successfully set to {self.current_budget:.2f}!\n\n" +
                          "You can now add items and calculate the best selection.\n" +
                          "Use 'Clear All' to reset the budget if needed.")
    
    def validate_name(self, name):
        if not name.strip():
            return False, "Item name cannot be empty!"
        if name.lower() in [item.lower() for item in self.items]: #Case-insensitive
            return False, "Item name already exists!"
        return True, ""
    
    def validate_price(self, price_str):
        try:
            price = float(price_str)
            if price <= 0:
                return False, "Price must be greater than 0!"
            
            if price >= 999999999:
                return False, "Price is msut be less than 999999999!"
            
            return True, price
        except ValueError:
            return False, "Price must be a valid number!"
    
    def validate_importance(self, importance_str):
        try:
            importance = int(importance_str)
            if importance < 1 or importance > 10:
                return False, "Importance must be between 1 and 10!"
            return True, importance
        except ValueError:
            return False, "Importance must be a whole number!"
    
    def validate_budget(self, budget_str):
        
        try:
            budget = float(budget_str)
            if budget <= 0:
                return False, "Budget must be greater than 0!"
            if budget >= 999999999:
                return False, "Budget must be less than 999999999!"
            return True, budget
        except ValueError:
            return False, "Budget must be a valid number!"
    
    def add_item(self):

        if not self.budget_set:
            messagebox.showerror("Budget Not Set", "Please set your budget first before adding items!")
            return
        
        name = self.name_entry.get()
        price_str = self.price_entry.get()
        importance_str = self.importance_entry.get()
        
        #Check name
        name_valid, name_msg = self.validate_name(name)
        if not name_valid:
            messagebox.showerror("Invalid Name", name_msg)
            return
        
        #Check price
        price_valid, price_result = self.validate_price(price_str)
        if not price_valid:
            messagebox.showerror("Invalid Price", price_result)
            return
        
        # Validate importance
        importance_valid, importance_result = self.validate_importance(importance_str)
        if not importance_valid:
            messagebox.showerror("Invalid Importance", importance_result)
            return
        
        # Add item to lists
        self.items.append(name.strip())
        self.prices.append(price_result)
        self.importance.append(importance_result)
        
        # Update display
        self.update_items_display()
        
        # Clear entry fields
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.importance_entry.delete(0, tk.END)
        
        # Show success message
        messagebox.showinfo("Success", f"'{name.strip()}' added successfully!")
    
    def update_items_display(self):
 
        self.items_text.config(state='normal')  # Enable editing temporarily
        self.items_text.delete(1.0, tk.END)
        
        if not self.items:
            self.items_text.insert(1.0, "No items added yet...\n\nAdd some items using the form above to get started!")
        else:
            self.items_text.insert(1.0, "Current Items:\n" + "="*50 + "\n\n")
            
            for i in range(len(self.items)):
                item_info = f"{i+1}. {self.items[i]} - {self.prices[i]:.2f} (importance: {self.importance[i]})\n"
                self.items_text.insert(tk.END, item_info)
            
            total_items = len(self.items)
            total_value = sum(self.prices)
            avg_importance = sum(self.importance) / len(self.importance)
            
            self.items_text.insert(tk.END, f"\n{'-'*50}\n")
            self.items_text.insert(tk.END, f"Total Items: {total_items}\n")
            self.items_text.insert(tk.END, f"Total Value: {total_value:.2f}\n")
            self.items_text.insert(tk.END, f"Average Importance: {avg_importance:.1f}")
        
        self.items_text.config(state='disabled')  # Disable editing
    
    def update_results_display(self, message):
        self.results_text.config(state='normal')  # Enable editing temporarily
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, message)
        self.results_text.config(state='disabled')  # Disable editing
    
    def show_results_popup(self, budget_result):
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Calculation Results")
        popup.geometry("500x400")
        popup.resizable(False, False)
        popup.configure(bg="#0F172A")
        popup.transient(self.root)  # Make it stay on top of main window
        popup.grab_set()  
        
        # Center the popup
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"500x400+{x}+{y}")
        
        if best_items:
            # Success case
            total_cost = sum(self.prices[self.items.index(item)] for item in best_items)
            
            # Title
            title_label = tk.Label(popup, text=" CALCULATION COMPLETE!", 
                                 font=('Times New Roman', 18, 'bold'), 
                                 bg='#0F172A', fg='#10B981')
            title_label.pack(pady=15)
            
            # Results frame
            results_frame = tk.LabelFrame(popup, text="Best Selection Found", 
                                        font=('Times New Roman', 14, 'bold'), 
                                        bg='#1E293B', fg='#F9FAFB', 
                                        padx=15, pady=15, relief='raised', bd=3)
            results_frame.pack(pady=10, padx=20, fill='both', expand=True)
            
            # Results text
            results_text = scrolledtext.ScrolledText(results_frame, height=12, width=55,
                                                   font=('Times New Roman', 11), 
                                                   bg='#E6FFFA', fg='#065F46',
                                                   state='normal', wrap='word')
            results_text.pack(fill='both', expand=True, pady=5)
            
            # Build results content
            results_content = f" OPTIMIZATION SUCCESSFUL!\n{'='*40}\n\n"
            results_content += f"Selected Items ({len(best_items)} total):\n"
            
            for i, item_name in enumerate(best_items):
                item_index = self.items.index(item_name)
                item_price = self.prices[item_index]
                item_imp = self.importance[item_index]
                results_content += f"  {i+1}. {item_name}\nPrice: {item_price:.2f}\nImportance: {item_imp}/10\n\n"
            
            results_content += f"{'-'*40}\n"
            results_content += f" Total Cost: {total_cost:.2f}\n"
            results_content += f" Budget Used: {budget_result:.2f}\n"
            results_content += f" Money Remaining: {budget_result - total_cost:.2f}\n"
            results_content += f" This is the optimal selection within your budget!"
            
            results_text.insert(1.0, results_content)
            results_text.config(state='disabled')
            
        else:
            # No solution case
            title_label = tk.Label(popup, text=" NO SOLUTION FOUND", 
                                 font=('Times New Roman', 18, 'bold'), 
                                 bg='#0F172A', fg='#EF4444')
            title_label.pack(pady=15)
            
            # Error frame
            error_frame = tk.LabelFrame(popup, text="Budget Insufficient", 
                                      font=('Times New Roman', 14, 'bold'), 
                                      bg='#1E293B', fg='#F9FAFB', 
                                      padx=15, pady=15, relief='raised', bd=3)
            error_frame.pack(pady=10, padx=20, fill='both', expand=True)
            
            # Error text
            error_text = scrolledtext.ScrolledText(error_frame, height=12, width=55,
                                                 font=('Times New Roman', 11), 
                                                 bg='#FEF2F2', fg='#991B1B',
                                                 state='normal', wrap='word')
            error_text.pack(fill='both', expand=True, pady=5)
            
            # Build error content
            error_content = f"Budget Too Low!\n{'='*40}\n\n"
            error_content += f"Your Budget: {budget_result:.2f}\n\n"
            
            if self.items:
                min_price = min(self.prices)
                min_index = self.prices.index(min_price)
                cheapest_item = self.items[min_index]
                error_content += f"Cheapest Available Item:\n"
                error_content += f"• {cheapest_item}: {min_price:.2f}\n\n"
                
                error_content += f" SUGGESTIONS:\n{'-'*30}\n"
                error_content += f"1. Increase budget to at least {min_price:.2f}\n"
                error_content += f"2. Add cheaper items to your list\n"
                error_content += f"3. Remove expensive items\n"
                error_content += f"4. Consider items with lower importance\n\n"
                
                # Show all items with prices
                error_content += f"All Available Items:\n{'-'*20}\n"
                for i, item in enumerate(self.items):
                    error_content += f"• {item}: {self.prices[i]:.2f} (imp: {self.importance[i]})\n"
            
            error_text.insert(1.0, error_content)
            error_text.config(state='disabled')
        
        # Close button
        close_btn = tk.Button(popup, text="Close", command=popup.destroy,
                            bg='#6B7280', fg='#F9FAFB', 
                            font=('Times New Roman', 12, 'bold'),
                            padx=25, pady=5, relief='raised', bd=3,
                            activebackground='#4B5563', activeforeground='#F9FAFB')
        close_btn.pack(pady=10)
        
        # Focus on popup
        popup.focus_set()

    def calculate(self):
        #Calculate best selection using backtracking
        global best_items, best_importance
        
        # Check if budget is set
        if not self.budget_set:
            messagebox.showerror("Budget Not Set", "Please set your budget first before calculating!")
            return
        
        # Check if enough items exist (minimum 2)
        if len(self.items) < 2:
            messagebox.showerror("Not Enough Items", 
                               f"You need at least 2 items to calculate the best selection.\n" +
                               f"Current items: {len(self.items)}\n" +
                               f"Please add {2 - len(self.items)} more item(s).")
            return
        
        # Reset best solution
        best_items = []
        best_importance = 0
        
        # Show calculating message
        self.update_results_display(" Calculating best selection... Please wait.")
        self.root.update_idletasks()  # Force GUI update
        
        # Run backtracking algorithm
        try:
            print(f"Starting calculation with {len(self.items)} items and budget {self.current_budget}")
            
            # Run the backtracking algorithm
            backtrack(self.items, self.prices, self.importance, 0, self.current_budget, [], 0)
            

            
            # Display results in main window first
            self.display_results(self.current_budget)
            
            # Force GUI update before showing popup
            self.root.update()
            self.root.update_idletasks()
            
            # Show custom results popup
            self.show_results_popup(self.current_budget)
                
        except Exception as e:
            print(f"Error during calculation: {e}")
            messagebox.showerror("Calculation Error", f"An error occurred during calculation:\n{str(e)}")
            self.update_results_display(" Calculation failed. Please try again.")
    
    def display_results(self, budget):
        self.results_text.config(state='normal')  # Enable editing temporarily
        self.results_text.delete(1.0, tk.END)
        
        if not best_items:
            self.results_text.insert(1.0, " NO ITEMS FIT WITHIN BUDGET!\n")
            self.results_text.insert(tk.END, "="*40 + "\n\n")
            self.results_text.insert(tk.END, f"Your Budget: {budget:.2f}\n")
            
            # Find cheapest item
            if self.items:
                min_price = min(self.prices)
                min_index = self.prices.index(min_price)
                cheapest_item = self.items[min_index]
                self.results_text.insert(tk.END, f"Cheapest Item: {cheapest_item} ({min_price:.2f})\n\n")
                self.results_text.insert(tk.END, " Suggestions:\n")
                self.results_text.insert(tk.END, f"• Clear all and set a higher budget (at least {min_price:.2f})\n")
                self.results_text.insert(tk.END, "• Add cheaper items to your list\n")
                self.results_text.insert(tk.END, "• Remove some expensive items")
        else:
            # Calculate total cost
            total_cost = 0
            for item_name in best_items:
                item_index = self.items.index(item_name)
                total_cost += self.prices[item_index]
            
            # Display best selection
            self.results_text.insert(1.0, " BEST SELECTION FOUND!\n")
            self.results_text.insert(tk.END, "="*40 + "\n\n")
            self.results_text.insert(tk.END, "Selected Items:\n")
            
            for i, item_name in enumerate(best_items):
                # Find item details
                item_index = self.items.index(item_name)
                item_price = self.prices[item_index]
                item_imp = self.importance[item_index]
                
                self.results_text.insert(tk.END, f"✓ {item_name} - {item_price:.2f} (importance: {item_imp})\n")
            
            self.results_text.insert(tk.END, "\n" + "-"*30 + "\n")
            self.results_text.insert(tk.END, f" Total Cost: {total_cost:.2f}\n")
            self.results_text.insert(tk.END, f" Money Left: {budget - total_cost:.2f}\n")
            self.results_text.insert(tk.END, f" Budget Used: {(total_cost/budget)*100:.1f}%\n")
            
        
        self.results_text.config(state='disabled')  # Disable editing
    
    def clear_all(self):
        if not self.items and not self.budget_set:
            messagebox.showinfo("Nothing to Clear", "There's no data to clear!")
            return
            
        budget_text = f"{self.current_budget:.2f}" if self.budget_set else "None"
        result = messagebox.askyesno("Confirm Clear", 
                                   "Are you sure you want to clear all data?\n\n" +
                                   "This will remove:\n" +
                                   f"• {len(self.items)} items from your cart\n" +
                                   f"• Your budget setting: {budget_text}\n" +
                                   "• All calculation results\n\n" +
                                   "You'll be able to set a new budget after clearing.")
        if result:
            self.items.clear()
            self.prices.clear()
            self.importance.clear()
            
            # Reset budget settings
            self.budget_set = False
            self.current_budget = 0.0
            
            # Re-enable budget input
            self.budget_entry.config(state='normal', bg='#E6FFFA')
            self.set_budget_btn.config(state='normal', bg='#10B981')
            self.budget_status_label.config(text="Enter budget and click 'Set Budget'", fg='#94A3B8')
            
            # Clear all entry fields
            self.budget_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.importance_entry.delete(0, tk.END)
            
            self.update_items_display()
            self.update_results_display(" All data cleared successfully!\n\nReady for new calculation. Set budget and add items to begin.")
            
            messagebox.showinfo("Cleared", "All data has been cleared successfully!\n\nYou can now set a new budget.")


def main():
    root = tk.Tk()
    app = KnapsackGUI(root)
    root.mainloop()


main()