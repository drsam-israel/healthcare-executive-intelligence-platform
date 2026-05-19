def generate_executive_response(
    question,
    total_admissions,
    readmission_rate,
    average_los,
    emergency_rate,
    bed_occupancy_rate,
    icu_occupancy_rate
):
    question_lower = question.lower()

    if "readmission" in question_lower:
        return f"""
        Readmission risk is currently estimated at {readmission_rate:.2f}% within the selected cohort.

        Key executive interpretation:
        - This reflects recurrent utilization burden.
        - High-risk cohorts may require enhanced discharge coordination.
        - Medication complexity, inpatient history, and emergency utilization are likely operational contributors.

        Recommended action:
        - Prioritize transitional care workflows.
        - Strengthen post-discharge follow-up.
        - Monitor moderate-risk and high-risk patients more closely.
        """

    elif "bed" in question_lower or "occupancy" in question_lower:
        return f"""
        Estimated bed occupancy is currently {bed_occupancy_rate:.1f}%, while ICU occupancy is approximately {icu_occupancy_rate:.1f}%.

        Key executive interpretation:
        - Bed occupancy reflects inpatient capacity pressure.
        - Higher LOS and recurrent utilization can worsen throughput.
        - ICU pressure may require proactive staffing and discharge planning.

        Recommended action:
        - Monitor occupancy thresholds.
        - Accelerate discharge planning for stable patients.
        - Use forecasting outputs for capacity readiness.
        """

    elif "emergency" in question_lower or "ed" in question_lower:
        return f"""
        Emergency-related admissions account for approximately {emergency_rate:.2f}% of the selected cohort.

        Key executive interpretation:
        - High ED dependency may suggest insufficient outpatient stabilization.
        - Emergency-origin utilization can increase cost and operational strain.
        - Chronic disease management pathways may need strengthening.

        Recommended action:
        - Expand outpatient diabetic stabilization programs.
        - Improve ED diversion workflows.
        - Strengthen care coordination for recurrent utilizers.
        """

    elif "los" in question_lower or "length of stay" in question_lower:
        return f"""
        Average length of stay is currently {average_los:.2f} days in the selected cohort.

        Key executive interpretation:
        - LOS directly influences bed occupancy and operating cost.
        - Prolonged stays may reflect clinical complexity or discharge bottlenecks.
        - LOS reduction can improve throughput and bed availability.

        Recommended action:
        - Review discharge delays.
        - Optimize inpatient care pathways.
        - Monitor high-LOS patient cohorts.
        """

    elif "forecast" in question_lower:
        return f"""
        Forecasting intelligence suggests that rising admissions and occupancy pressure should be monitored proactively.

        Key executive interpretation:
        - Capacity pressure may increase if admissions grow over the next 4 weeks.
        - Bed occupancy and ICU occupancy should be reviewed alongside staffing and discharge readiness.
        - Forecasting supports proactive operational planning.

        Recommended action:
        - Prepare staffing plans.
        - Strengthen discharge coordination.
        - Monitor occupancy thresholds weekly.
        """

    elif "recommend" in question_lower or "strategy" in question_lower:
        return f"""
        Executive recommendations based on the selected cohort:

        - Expand transitional care coordination for high-risk diabetic patients.
        - Strengthen outpatient chronic disease management.
        - Implement medication reconciliation for complex medication profiles.
        - Use bed occupancy intelligence for capacity planning.
        - Integrate predictive and explainable AI into operational review meetings.
        """

    else:
        return f"""
        Executive summary for the selected cohort:

        - Total admissions analyzed: {total_admissions:,}
        - Readmission burden: {readmission_rate:.2f}%
        - Average LOS: {average_los:.2f} days
        - Emergency admission burden: {emergency_rate:.2f}%
        - Estimated bed occupancy: {bed_occupancy_rate:.1f}%
        - Estimated ICU occupancy: {icu_occupancy_rate:.1f}%

        This cohort should be reviewed for utilization burden, readmission risk, bed capacity pressure, and opportunities for operational improvement.
        """