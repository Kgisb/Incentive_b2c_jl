#!/usr/bin/env python
# coding: utf-8

# In[35]:


import ipywidgets as widgets
from IPython.display import display, clear_output

def calculate_cash_in_incentive(total_upfront_cash_in):
    conversion_rate = 88  # Conversion value from Euro to INR
    if 499 <= total_upfront_cash_in < 999:
        return 0
    elif 999 <= total_upfront_cash_in < 1499:
        return 0.015 * total_upfront_cash_in * conversion_rate
    elif 1499 <= total_upfront_cash_in < 1999:
        return 0.025 * total_upfront_cash_in * conversion_rate
    elif 1999 <= total_upfront_cash_in < 2499:
        return 0.05 * total_upfront_cash_in * conversion_rate
    elif 2499 <= total_upfront_cash_in < 2999:
        return 0.075 * total_upfront_cash_in * conversion_rate
    elif 2999 <= total_upfront_cash_in < 3499:
        return 0.1 * total_upfront_cash_in * conversion_rate
    elif 3499 <= total_upfront_cash_in < 3999:
        return 0.125 * total_upfront_cash_in * conversion_rate
    elif total_upfront_cash_in >= 3999:
        return 0.15 * total_upfront_cash_in * conversion_rate
    else:
        return 0

def calculate_price_control_incentive(full_payment_cash_in, mrp, deal_source):
    conversion_rate = 88  # Conversion value from Euro to INR
    if deal_source in ["PM-Search", "PM-Social", "Organic", "Others"]:
        if mrp == 649 and full_payment_cash_in >= 449:
            return 0.075 * (full_payment_cash_in / mrp) * conversion_rate * full_payment_cash_in
        elif mrp == 1199 and full_payment_cash_in >= 899:
            return 0.075 * (full_payment_cash_in / mrp) * conversion_rate * full_payment_cash_in
        elif mrp == 1999 and full_payment_cash_in >= 1549:
            return 0.075 * (full_payment_cash_in / mrp) * conversion_rate * full_payment_cash_in
        else:
            return 0
    elif deal_source in ["Referral", "Events", "Goldmine", "DP"]:
        if mrp == 649 and full_payment_cash_in >= 399:
            return 0.075 * (full_payment_cash_in / mrp) * conversion_rate * full_payment_cash_in
        elif mrp == 1199 and full_payment_cash_in >= 799:
            return 0.075 * (full_payment_cash_in / mrp) * conversion_rate * full_payment_cash_in
        elif mrp == 1999 and full_payment_cash_in >= 1429:
            return 0.075 * (full_payment_cash_in / mrp) * conversion_rate * full_payment_cash_in
        else:
            return 0
    else:
        return 0

def display_interface():
    # Upfront Cash-in Section
    upfront_cash_in_widget = widgets.FloatText(description="Total Upfront Cash-in (€):", value=0)
    calculate_upfront_button = widgets.Button(description="Calculate Upfront Incentive")
    upfront_output = widgets.Output()

    def calculate_upfront_incentive(b):
        with upfront_output:
            clear_output()
            upfront_cash_in = upfront_cash_in_widget.value
            upfront_incentive = calculate_cash_in_incentive(upfront_cash_in)
            print(f"Upfront Cash-in Incentive: INR {upfront_incentive:,.2f}")

    calculate_upfront_button.on_click(calculate_upfront_incentive)

    # Full Payment Section (Price Control Incentive)
    full_payment_entries = []

    def add_full_payment_entry():
        full_payment_cash_in_widget = widgets.FloatText(description="Full Payment Cash-in (€):", value=0)
        mrp_widget = widgets.Dropdown(
            description="MRP (€):",
            options=[119, 349, 649, 1199, 1999],
            value=119
        )
        deal_source_widget = widgets.Dropdown(
            description="Deal Source:",
            options=["PM-Search", "PM-Social", "Organic", "Others", "Referral", "Events", "Goldmine", "DP"],
            value="PM-Search"
        )
        price_control_output = widgets.Output()
        calculate_button = widgets.Button(description="Calculate Incentive")
        delete_entry_button = widgets.Button(description="Delete Entry", button_style="danger")

        def calculate_price_control(b):
            with price_control_output:
                clear_output()
                full_payment_cash_in = full_payment_cash_in_widget.value
                mrp = mrp_widget.value
                deal_source = deal_source_widget.value
                price_control_incentive = calculate_price_control_incentive(full_payment_cash_in, mrp, deal_source)
                print(f"Price Control Incentive: INR {price_control_incentive:,.2f}")

        def delete_entry(b):
            full_payment_entries.remove(entry)
            entry.close()

        calculate_button.on_click(calculate_price_control)
        delete_entry_button.on_click(delete_entry)

        entry = widgets.VBox([
            full_payment_cash_in_widget,
            mrp_widget,
            deal_source_widget,
            widgets.HBox([calculate_button, delete_entry_button]),
            price_control_output
        ])

        full_payment_entries.append(entry)
        display(entry)

    add_full_payment_checkbox = widgets.Checkbox(description="Add Another Full Payment Case", value=False)

    def on_add_full_payment_change(change):
        if change['new']:
            add_full_payment_entry()
            add_full_payment_checkbox.value = False

    add_full_payment_checkbox.observe(on_add_full_payment_change, names='value')

    # Additional Incentives Section
    d0_conversion_widget = widgets.IntText(description="D0 Conversion Cases >= €400:", value=0)
    within_window_widget = widgets.IntText(description="Converted within Window Cases:", value=0)
    self_gen_referral_widget = widgets.IntText(description="Self Gen Referral Cases:", value=0)
    calculate_additional_button = widgets.Button(description="Calculate Additional Incentives")
    additional_output = widgets.Output()

    def calculate_additional_incentives(b):
        with additional_output:
            clear_output()
            d0_cases = d0_conversion_widget.value
            within_window_cases = within_window_widget.value
            self_gen_cases = self_gen_referral_widget.value
            additional_incentive = (d0_cases * 300) + (within_window_cases * 4000) + (self_gen_cases * 3000)
            print(f"Additional Incentives: INR {additional_incentive:,.2f}")

    calculate_additional_button.on_click(calculate_additional_incentives)

    # Final Calculation Section
    calculate_final_button = widgets.Button(description="Calculate Total Incentive", button_style="success")
    final_output = widgets.Output()

    def calculate_final_incentive(b):
        with final_output:
            clear_output()
            upfront_cash_in = upfront_cash_in_widget.value
            upfront_incentive = calculate_cash_in_incentive(upfront_cash_in)

            total_price_control_incentive = 0
            for entry in full_payment_entries:
                full_payment_cash_in = entry.children[0].value
                mrp = entry.children[1].value
                deal_source = entry.children[2].value
                total_price_control_incentive += calculate_price_control_incentive(full_payment_cash_in, mrp, deal_source)

            d0_cases = d0_conversion_widget.value
            within_window_cases = within_window_widget.value
            self_gen_cases = self_gen_referral_widget.value
            additional_incentive = (d0_cases * 300) + (within_window_cases * 4000) + (self_gen_cases * 3000)

            total_incentive = upfront_incentive + total_price_control_incentive + additional_incentive
            with final_output:
                clear_output()
                display(widgets.HTML(f"<h2 style='color: blue; text-align: center;'>Overall Total Incentive: INR {total_incentive:,.2f}</h2>"))

    calculate_final_button.on_click(calculate_final_incentive)

    # Layout for Incentive Calculator and Final Output
    incentive_calculator_section = widgets.VBox([
        widgets.Label("Incentive Calculator", style={'font-weight': 'bold', 'font-size': '16px'}),
        widgets.Label("Upfront Cash-in Incentive Calculation"),
        upfront_cash_in_widget,
        calculate_upfront_button,
        upfront_output,

        widgets.Label("Price Control Incentive Calculation"),
        add_full_payment_checkbox,

        widgets.Label("Additional Incentives Calculation"),
        d0_conversion_widget,
        within_window_widget,
        self_gen_referral_widget,
        calculate_additional_button,
        additional_output,
    ])

    final_incentive_section = widgets.VBox([
        widgets.Label("Final Incentive", style={'font-weight': 'bold', 'font-size': '16px'}),
        calculate_final_button,
        final_output
    ])

    main_layout = widgets.HBox([
        incentive_calculator_section,
        final_incentive_section
    ], layout=widgets.Layout(justify_content="space-between"))

    display(main_layout)

# Run the interactive interface
display_interface()


# In[ ]:




