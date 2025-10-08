"""
Smart Scheduling Suggestions System
Analyzes posting history to recommend optimal posting times
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
import statistics


class SchedulingAI:
    """AI-powered scheduling suggestions based on historical data"""

    def __init__(self):
        self.posting_history = []

    def add_post_result(self, post_data: Dict):
        """Record a post result for analysis"""
        self.posting_history.append({
            'timestamp': post_data.get('timestamp', datetime.now().isoformat()),
            'scheduled_time': post_data.get('schedule_time'),
            'completed_at': post_data.get('completed_at'),
            'status': post_data.get('status', 'unknown'),
            'models': post_data.get('models', []),
            'engagement': post_data.get('engagement', 0)
        })

    def get_optimal_times(self, num_suggestions: int = 5) -> List[Dict]:
        """
        Analyze posting history to suggest optimal posting times

        Returns list of suggested times with confidence scores
        """
        if len(self.posting_history) < 10:
            # Not enough data - return default optimal times
            return self._get_default_suggestions()

        # Analyze successful posts by time of day and day of week
        time_performance = defaultdict(list)

        for post in self.posting_history:
            if post['status'] == 'completed' and post['completed_at']:
                completed = datetime.fromisoformat(post['completed_at'])
                hour = completed.hour
                day_of_week = completed.weekday()

                key = (day_of_week, hour)
                time_performance[key].append({
                    'engagement': post.get('engagement', 0),
                    'success': 1
                })

        # Calculate average performance for each time slot
        performance_scores = []
        for (day, hour), posts in time_performance.items():
            avg_engagement = statistics.mean([p['engagement'] for p in posts])
            success_rate = sum([p['success'] for p in posts]) / len(posts)

            performance_scores.append({
                'day_of_week': day,
                'hour': hour,
                'avg_engagement': avg_engagement,
                'success_rate': success_rate,
                'sample_size': len(posts),
                'confidence': min(100, len(posts) * 10)  # Higher confidence with more data
            })

        # Sort by engagement and success rate
        performance_scores.sort(
            key=lambda x: (x['avg_engagement'] * x['success_rate'], x['sample_size']),
            reverse=True
        )

        # Generate suggestions
        suggestions = []
        for score in performance_scores[:num_suggestions]:
            next_occurrence = self._get_next_occurrence(score['day_of_week'], score['hour'])

            suggestions.append({
                'datetime': next_occurrence.isoformat(),
                'day_name': next_occurrence.strftime('%A'),
                'time': next_occurrence.strftime('%I:%M %p'),
                'confidence': score['confidence'],
                'avg_engagement': round(score['avg_engagement'], 2),
                'success_rate': round(score['success_rate'] * 100, 1),
                'reason': self._generate_reason(score)
            })

        return suggestions

    def _get_default_suggestions(self) -> List[Dict]:
        """Return default optimal posting times when insufficient data"""
        default_times = [
            {'day': 0, 'hour': 10, 'reason': 'Monday morning - high engagement'},
            {'day': 2, 'hour': 14, 'reason': 'Wednesday afternoon - consistent performance'},
            {'day': 3, 'hour': 19, 'reason': 'Thursday evening - peak activity'},
            {'day': 5, 'hour': 11, 'reason': 'Saturday late morning - weekend engagement'},
            {'day': 6, 'hour': 15, 'reason': 'Sunday afternoon - relaxed browsing'},
        ]

        suggestions = []
        for default in default_times:
            next_time = self._get_next_occurrence(default['day'], default['hour'])

            suggestions.append({
                'datetime': next_time.isoformat(),
                'day_name': next_time.strftime('%A'),
                'time': next_time.strftime('%I:%M %p'),
                'confidence': 50,  # Medium confidence for defaults
                'avg_engagement': 0,
                'success_rate': 0,
                'reason': default['reason']
            })

        return suggestions

    def _get_next_occurrence(self, target_day: int, target_hour: int) -> datetime:
        """Get the next occurrence of a specific day and hour"""
        now = datetime.now()
        days_ahead = target_day - now.weekday()

        if days_ahead < 0:  # Target day already happened this week
            days_ahead += 7
        elif days_ahead == 0 and now.hour >= target_hour:  # Same day but hour passed
            days_ahead = 7

        next_date = now + timedelta(days=days_ahead)
        return next_date.replace(hour=target_hour, minute=0, second=0, microsecond=0)

    def _generate_reason(self, score: Dict) -> str:
        """Generate human-readable reason for suggestion"""
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = day_names[score['day_of_week']]

        if score['hour'] < 12:
            time_period = 'morning'
        elif score['hour'] < 17:
            time_period = 'afternoon'
        else:
            time_period = 'evening'

        engagement_level = 'high' if score['avg_engagement'] > 5 else 'good'

        return f"{day_name} {time_period} - {engagement_level} engagement ({score['sample_size']} posts)"

    def analyze_posting_patterns(self) -> Dict:
        """Analyze overall posting patterns and provide insights"""
        if len(self.posting_history) < 5:
            return {
                'status': 'insufficient_data',
                'message': 'Need at least 5 posts to analyze patterns'
            }

        # Analyze by day of week
        day_performance = defaultdict(list)
        hour_performance = defaultdict(list)

        for post in self.posting_history:
            if post['status'] == 'completed' and post['completed_at']:
                completed = datetime.fromisoformat(post['completed_at'])

                day_performance[completed.weekday()].append(post.get('engagement', 0))
                hour_performance[completed.hour].append(post.get('engagement', 0))

        # Calculate averages
        best_day = max(day_performance.items(), key=lambda x: statistics.mean(x[1]))
        best_hour = max(hour_performance.items(), key=lambda x: statistics.mean(x[1]))

        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        return {
            'status': 'success',
            'total_posts': len(self.posting_history),
            'best_day': {
                'day': day_names[best_day[0]],
                'avg_engagement': round(statistics.mean(best_day[1]), 2)
            },
            'best_hour': {
                'hour': best_hour[0],
                'formatted': f"{best_hour[0]:02d}:00",
                'avg_engagement': round(statistics.mean(best_hour[1]), 2)
            },
            'insights': [
                f"Your best posting day is {day_names[best_day[0]]}",
                f"Optimal posting time is around {best_hour[0]:02d}:00",
                f"Total posts analyzed: {len(self.posting_history)}"
            ]
        }


# Global instance
scheduling_ai = SchedulingAI()
