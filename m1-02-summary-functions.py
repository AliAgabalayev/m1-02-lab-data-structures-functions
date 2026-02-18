def findAverageForPerCategory(logs):
    category_resolution_times = {}
    for log in logs:
        catType = log.get("category")
        if catType not in category_resolution_times:
            category_resolution_times[catType] = [0.0, 0]
        category_resolution_times[catType][0] += log.get("resolution_minutes")
        category_resolution_times[catType][1] += 1

    average_for_per_category = {catType: (round(val[0] / val[1], 2)) for catType, val in
                                category_resolution_times.items()}

    return average_for_per_category

def findEscalationRate(logs):
    true_count_per_category = {}
    overall_true_count = 0
    for log in logs:
        catType = log.get("category")
        if catType not in true_count_per_category:
            true_count_per_category[catType] = [0,0]
        if log.get("escalated"):
            true_count_per_category[catType][0] += 1
            overall_true_count += 1
        true_count_per_category[catType][1] += 1

    escalation_rate_per_category = {catType :(round(val[0]/val[1],2)) for catType, val in true_count_per_category.items() }
    escalation_rate_per_category["overall"] = overall_true_count/len(logs)

    return escalation_rate_per_category

def findTicketsPerCustomer(logs):
    tickets_count_for_per_customer = {}
    for log in logs:
        customerId = log.get("customer_id")
        if customerId not in tickets_count_for_per_customer:
            tickets_count_for_per_customer[customerId] = 0
        tickets_count_for_per_customer[customerId] += 1
    return tickets_count_for_per_customer


def validate_ticket_count(customer_counts, original_logs):
    total_counted = sum(customer_counts.values())
    is_valid = (total_counted == len(original_logs))

    if is_valid:
        print("✅ Validation 1 (Ticket Counts): True")
    else:
        print(f"❌ Validation 1 (Ticket Counts): False. Counted {total_counted}, expected {len(original_logs)}")

    return is_valid


def validate_category_consistency(summary_data, original_logs):
    summary_keys = set(summary_data.keys())

    log_categories = set(log.get("category") for log in original_logs)

    is_valid = (summary_keys == log_categories)

    if is_valid:
        print("✅ Validation 2 (Categories): True")
    else:
        print(f"❌ Validation 2 (Categories): False. Mismatch found.")
        print(f"   In Summary: {summary_keys}")
        print(f"   In Logs: {log_categories}")

    return is_valid


def validate_rate_range(rate_data):
    invalid_rates = {k: v for k, v in rate_data.items() if not (0.0 <= v <= 1.0)}

    if not invalid_rates:
        print("✅ Validation 3 (Rate Range): True")
        return True
    else:
        print(f"❌ Validation 3 (Rate Range): False. Invalid values found: {invalid_rates}")
        return False