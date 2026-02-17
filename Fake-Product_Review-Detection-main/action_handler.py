from datetime import datetime
import json
import os

class ReviewActionHandler:
    """Handle actions based on fake review predictions"""
    
    def __init__(self, action_log_dir='actions'):
        os.makedirs(action_log_dir, exist_ok=True)
        self.action_log = f"{action_log_dir}/actions_{datetime.now().strftime('%Y%m%d')}.json"
        self.blocked_users = set()
        self.flagged_reviews = []
    
    def decide_action(self, review_id, prediction, confidence, user_id=None):
        """Decide what action to take based on prediction"""
        
        action = {
            'review_id': review_id,
            'timestamp': datetime.now().isoformat(),
            'prediction': prediction,
            'confidence': confidence,
            'user_id': user_id
        }
        
        if prediction == 'FAKE':
            if confidence >= 0.9:
                action['decision'] = 'REMOVE'
                action['reason'] = 'High confidence fake review'
                self._remove_review(review_id)
                
            elif confidence >= 0.7:
                action['decision'] = 'FLAG_FOR_REVIEW'
                action['reason'] = 'Likely fake, needs manual review'
                self._flag_review(review_id)
                
            elif confidence >= 0.5:
                action['decision'] = 'MONITOR'
                action['reason'] = 'Suspicious, monitor user activity'
                self._monitor_user(user_id)
                
        else:  # REAL
            if confidence >= 0.8:
                action['decision'] = 'PUBLISH'
                action['reason'] = 'Genuine review'
                self._publish_review(review_id)
            else:
                action['decision'] = 'MANUAL_REVIEW'
                action['reason'] = 'Uncertain, needs human verification'
        
        self._log_action(action)
        return action
    
    def _remove_review(self, review_id):
        """Remove fake review from platform"""
        print(f"🗑️ Removing review {review_id}")
        # Integration with e-commerce platform API
    
    def _flag_review(self, review_id):
        """Flag review for manual moderation"""
        print(f"🚩 Flagging review {review_id} for manual review")
        self.flagged_reviews.append(review_id)
    
    def _monitor_user(self, user_id):
        """Add user to monitoring list"""
        if user_id:
            print(f"👁️ Monitoring user {user_id}")
    
    def _publish_review(self, review_id):
        """Publish genuine review"""
        print(f"✅ Publishing review {review_id}")
    
    def block_user(self, user_id, reason):
        """Block repeat offender"""
        self.blocked_users.add(user_id)
        print(f"🔒 Blocked user {user_id}: {reason}")
        
        block_action = {
            'action': 'BLOCK_USER',
            'user_id': user_id,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
        self._log_action(block_action)
    
    def _log_action(self, action):
        """Log action to file"""
        try:
            if os.path.exists(self.action_log):
                with open(self.action_log, 'r') as f:
                    actions = json.load(f)
            else:
                actions = []
            
            actions.append(action)
            
            with open(self.action_log, 'w') as f:
                json.dump(actions, f, indent=2)
        except Exception as e:
            print(f"Error logging action: {e}")
    
    def get_flagged_reviews(self):
        """Get list of flagged reviews for manual review"""
        return self.flagged_reviews
    
    def get_statistics(self):
        """Get action statistics"""
        try:
            with open(self.action_log, 'r') as f:
                actions = json.load(f)
            
            stats = {
                'total_actions': len(actions),
                'removed': sum(1 for a in actions if a.get('decision') == 'REMOVE'),
                'flagged': sum(1 for a in actions if a.get('decision') == 'FLAG_FOR_REVIEW'),
                'published': sum(1 for a in actions if a.get('decision') == 'PUBLISH'),
                'blocked_users': len(self.blocked_users)
            }
            return stats
        except:
            return None
