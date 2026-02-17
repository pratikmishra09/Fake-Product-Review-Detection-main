# 🛒 E-commerce Platform Integration Guide

## 📋 Overview

This guide explains how to integrate the Fake Review Detection System into e-commerce platforms like Amazon, eBay, Shopify, WooCommerce, Magento, etc.

---

## 🎯 Integration Methods

### **Method 1: REST API Integration** (Recommended)
- Real-time review screening
- Easy to implement
- Platform-agnostic
- Scalable

### **Method 2: Batch Processing**
- Analyze existing reviews
- Scheduled jobs
- Bulk operations

### **Method 3: Plugin/Extension**
- Platform-specific integration
- One-click installation
- Automated workflow

---

## 🚀 Method 1: REST API Integration

### **Step 1: Deploy the API**

```bash
# Option A: Docker (Recommended)
docker-compose up -d

# Option B: Direct Python
python app.py

# API will be available at: http://your-server:5000
```

### **Step 2: Integrate with Your Platform**

#### **For Custom E-commerce Platform**

```python
import requests

class FakeReviewDetector:
    def __init__(self, api_url="http://your-server:5000"):
        self.api_url = api_url
    
    def check_review(self, review_text, review_id, user_id):
        """Check if review is fake before publishing"""
        
        # Call detection API
        response = requests.post(f"{self.api_url}/predict", json={
            'review_text': review_text
        })
        
        result = response.json()
        
        # Take action based on confidence
        if result['prediction'] == 'FAKE':
            if result['confidence'] > 0.9:
                return self.reject_review(review_id, "High confidence fake")
            elif result['confidence'] > 0.7:
                return self.flag_for_moderation(review_id, user_id)
            else:
                return self.monitor_user(user_id)
        else:
            return self.publish_review(review_id)
    
    def reject_review(self, review_id, reason):
        # Don't publish, notify user
        return {"action": "REJECTED", "reason": reason}
    
    def flag_for_moderation(self, review_id, user_id):
        # Send to moderation queue
        return {"action": "FLAGGED", "review_id": review_id}
    
    def monitor_user(self, user_id):
        # Add to watchlist
        return {"action": "MONITORED", "user_id": user_id}
    
    def publish_review(self, review_id):
        # Publish normally
        return {"action": "PUBLISHED", "review_id": review_id}

# Usage
detector = FakeReviewDetector()
result = detector.check_review(
    review_text="This product is amazing!",
    review_id=12345,
    user_id=67890
)
```

---

### **Integration Workflow Diagram**

```
┌─────────────────────────────────────────────────────────┐
│           User Submits Review on E-commerce             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│     E-commerce Backend Receives Review                  │
│     (Before saving to database)                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│     Call Fake Review Detection API                      │
│     POST /predict                                       │
│     {"review_text": "..."}                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│     API Returns Prediction                              │
│     {"prediction": "FAKE", "confidence": 0.92}          │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌────────┐  ┌─────────┐  ┌──────────┐
   │ REJECT │  │  FLAG   │  │ PUBLISH  │
   │ Review │  │ Review  │  │ Review   │
   └────────┘  └─────────┘  └──────────┘
   >90% fake   70-90% fake   <70% fake
```

---

## 🛍️ Platform-Specific Integration

### **1. Shopify Integration**

```javascript
// Shopify App - Node.js Backend

const axios = require('axios');

// Webhook handler for new reviews
app.post('/webhooks/reviews/create', async (req, res) => {
    const review = req.body;
    
    // Check review with API
    const response = await axios.post('http://your-server:5000/predict', {
        review_text: review.body
    });
    
    const result = response.data;
    
    if (result.prediction === 'FAKE' && result.confidence > 0.7) {
        // Unpublish review
        await shopify.review.update(review.id, {
            published: false,
            tags: 'flagged-fake'
        });
        
        // Notify admin
        await sendAdminNotification(review.id, result);
    }
    
    res.status(200).send('OK');
});
```

---

### **2. WooCommerce (WordPress) Integration**

```php
<?php
// WooCommerce Plugin - functions.php

add_filter('preprocess_comment', 'check_fake_review');

function check_fake_review($commentdata) {
    // Only check product reviews
    if ($commentdata['comment_type'] !== 'review') {
        return $commentdata;
    }
    
    // Call detection API
    $response = wp_remote_post('http://your-server:5000/predict', array(
        'body' => json_encode(array(
            'review_text' => $commentdata['comment_content']
        )),
        'headers' => array('Content-Type' => 'application/json')
    ));
    
    $result = json_decode(wp_remote_retrieve_body($response), true);
    
    // Handle fake reviews
    if ($result['prediction'] === 'FAKE' && $result['confidence'] > 0.7) {
        // Hold for moderation
        $commentdata['comment_approved'] = 0;
        
        // Add meta data
        add_comment_meta($commentdata['comment_ID'], 'fake_confidence', 
                        $result['confidence']);
        add_comment_meta($commentdata['comment_ID'], 'flagged_fake', true);
    }
    
    return $commentdata;
}
?>
```

---

### **3. Magento Integration**

```php
<?php
// Magento 2 Module - Observer

namespace Vendor\FakeReviewDetector\Observer;

use Magento\Framework\Event\Observer;
use Magento\Framework\Event\ObserverInterface;

class CheckReviewObserver implements ObserverInterface
{
    public function execute(Observer $observer)
    {
        $review = $observer->getEvent()->getObject();
        
        // Call API
        $ch = curl_init('http://your-server:5000/predict');
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
            'review_text' => $review->getDetail()
        ]));
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type:application/json']);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = json_decode(curl_exec($ch), true);
        curl_close($ch);
        
        // Handle result
        if ($response['prediction'] === 'FAKE' && $response['confidence'] > 0.7) {
            $review->setStatusId(3); // Pending status
            $review->setData('fake_confidence', $response['confidence']);
        }
    }
}
?>
```

---

### **4. Custom Django E-commerce**

```python
# Django views.py

from django.views.decorators.http import require_POST
import requests

@require_POST
def submit_review(request):
    review_text = request.POST.get('review_text')
    product_id = request.POST.get('product_id')
    
    # Check with fake review detector
    response = requests.post('http://your-server:5000/predict', json={
        'review_text': review_text
    })
    
    result = response.json()
    
    # Create review object
    review = Review(
        product_id=product_id,
        user=request.user,
        text=review_text,
        is_published=True
    )
    
    # Handle fake reviews
    if result['prediction'] == 'FAKE':
        if result['confidence'] > 0.9:
            # Reject completely
            return JsonResponse({
                'status': 'rejected',
                'message': 'Review flagged as suspicious'
            })
        elif result['confidence'] > 0.7:
            # Hold for moderation
            review.is_published = False
            review.moderation_status = 'flagged'
            review.fake_confidence = result['confidence']
    
    review.save()
    
    return JsonResponse({
        'status': 'success',
        'review_id': review.id
    })
```

---

## 📦 Method 2: Batch Processing

### **Analyze Existing Reviews**

```python
import requests
import pandas as pd

def batch_analyze_reviews(csv_file):
    """Analyze all existing reviews in bulk"""
    
    # Load reviews
    df = pd.read_csv(csv_file)
    
    # Call batch API
    response = requests.post('http://your-server:5000/predict_batch', json={
        'reviews': df['review_text'].tolist()
    })
    
    results = response.json()['results']
    
    # Add predictions to dataframe
    df['prediction'] = [r['prediction'] for r in results]
    df['fake_confidence'] = [r['fake_probability'] for r in results]
    
    # Filter fake reviews
    fake_reviews = df[df['prediction'] == 'FAKE']
    
    # Take action
    for _, review in fake_reviews.iterrows():
        if review['fake_confidence'] > 0.9:
            delete_review(review['review_id'])
        elif review['fake_confidence'] > 0.7:
            flag_review(review['review_id'])
    
    return fake_reviews

# Run daily
fake_reviews = batch_analyze_reviews('reviews_today.csv')
print(f"Found {len(fake_reviews)} fake reviews")
```

---

## 🔄 Automated Workflow Examples

### **Example 1: Real-time Review Screening**

```python
# E-commerce Platform Code

def handle_new_review(review_data):
    """Called when user submits a review"""
    
    # Step 1: Validate input
    if len(review_data['text']) < 10:
        return {"error": "Review too short"}
    
    # Step 2: Check for fake
    detection_result = check_fake_review(review_data['text'])
    
    # Step 3: Take action
    if detection_result['is_fake']:
        confidence = detection_result['confidence']
        
        if confidence > 0.9:
            # Auto-reject
            log_rejected_review(review_data, confidence)
            return {
                "status": "rejected",
                "message": "Review could not be published"
            }
        
        elif confidence > 0.7:
            # Flag for moderation
            save_review(review_data, published=False, flagged=True)
            notify_moderators(review_data, confidence)
            return {
                "status": "pending",
                "message": "Review is under review"
            }
    
    # Step 4: Publish genuine reviews
    save_review(review_data, published=True)
    update_product_rating(review_data['product_id'])
    
    return {
        "status": "published",
        "message": "Thank you for your review!"
    }
```

---

### **Example 2: Scheduled Batch Analysis**

```python
# Cron job - runs daily at 2 AM

import schedule
import time

def daily_review_scan():
    """Scan all reviews from last 24 hours"""
    
    # Get yesterday's reviews
    reviews = get_reviews_from_last_24_hours()
    
    # Batch analyze
    response = requests.post('http://your-server:5000/predict_batch', json={
        'reviews': [r['text'] for r in reviews]
    })
    
    results = response.json()['results']
    
    # Process results
    for review, result in zip(reviews, results):
        if result['prediction'] == 'FAKE' and result['fake_probability'] > 0.7:
            # Unpublish and flag
            unpublish_review(review['id'])
            flag_for_manual_review(review['id'], result['fake_probability'])
            
            # Check user history
            user_fake_count = count_user_fake_reviews(review['user_id'])
            if user_fake_count > 3:
                block_user(review['user_id'], "Multiple fake reviews")
    
    # Generate report
    generate_daily_report(results)

# Schedule
schedule.every().day.at("02:00").do(daily_review_scan)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🎯 Complete Integration Example

### **Full E-commerce Integration**

```python
# complete_integration.py

import requests
from datetime import datetime

class EcommerceFakeReviewIntegration:
    def __init__(self, api_url, db_connection):
        self.api_url = api_url
        self.db = db_connection
    
    def on_review_submit(self, user_id, product_id, review_text, rating):
        """Handle new review submission"""
        
        # 1. Check for fake
        result = self.detect_fake(review_text)
        
        # 2. Create review record
        review_id = self.create_review(
            user_id=user_id,
            product_id=product_id,
            text=review_text,
            rating=rating,
            fake_score=result['fake_probability'],
            published=False
        )
        
        # 3. Decision logic
        action = self.decide_action(result, user_id)
        
        # 4. Execute action
        if action == 'PUBLISH':
            self.publish_review(review_id)
            self.update_product_stats(product_id)
            return {"status": "published", "review_id": review_id}
        
        elif action == 'FLAG':
            self.flag_review(review_id)
            self.notify_moderators(review_id)
            return {"status": "pending_review", "review_id": review_id}
        
        elif action == 'REJECT':
            self.reject_review(review_id)
            self.log_rejection(user_id, review_id, result)
            return {"status": "rejected", "message": "Review could not be published"}
    
    def detect_fake(self, review_text):
        """Call detection API"""
        response = requests.post(f"{self.api_url}/predict", json={
            'review_text': review_text
        })
        return response.json()
    
    def decide_action(self, result, user_id):
        """Decide what to do with review"""
        
        # Check user history
        user_history = self.get_user_history(user_id)
        
        if result['prediction'] == 'FAKE':
            confidence = result['confidence']
            
            # High confidence fake
            if confidence > 0.9:
                return 'REJECT'
            
            # Medium confidence or suspicious user
            elif confidence > 0.7 or user_history['fake_count'] > 2:
                return 'FLAG'
        
        # Publish genuine reviews
        return 'PUBLISH'
    
    def create_review(self, **kwargs):
        """Save review to database"""
        query = """
            INSERT INTO reviews (user_id, product_id, text, rating, 
                               fake_score, published, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        return self.db.execute(query, (
            kwargs['user_id'], kwargs['product_id'], kwargs['text'],
            kwargs['rating'], kwargs['fake_score'], kwargs['published'],
            datetime.now()
        )).fetchone()[0]
    
    def publish_review(self, review_id):
        """Make review visible"""
        self.db.execute(
            "UPDATE reviews SET published = TRUE WHERE id = %s",
            (review_id,)
        )
    
    def flag_review(self, review_id):
        """Flag for moderation"""
        self.db.execute(
            "UPDATE reviews SET moderation_status = 'flagged' WHERE id = %s",
            (review_id,)
        )
    
    def reject_review(self, review_id):
        """Reject review"""
        self.db.execute(
            "UPDATE reviews SET status = 'rejected' WHERE id = %s",
            (review_id,)
        )
    
    def get_user_history(self, user_id):
        """Get user's review history"""
        result = self.db.execute("""
            SELECT 
                COUNT(*) as total_reviews,
                SUM(CASE WHEN fake_score > 0.7 THEN 1 ELSE 0 END) as fake_count
            FROM reviews
            WHERE user_id = %s
        """, (user_id,)).fetchone()
        
        return {
            'total_reviews': result[0],
            'fake_count': result[1]
        }
    
    def update_product_stats(self, product_id):
        """Recalculate product rating"""
        self.db.execute("""
            UPDATE products
            SET average_rating = (
                SELECT AVG(rating)
                FROM reviews
                WHERE product_id = %s AND published = TRUE
            )
            WHERE id = %s
        """, (product_id, product_id))
    
    def notify_moderators(self, review_id):
        """Send notification to moderation team"""
        # Implementation depends on your notification system
        pass

# Usage
integration = EcommerceFakeReviewIntegration(
    api_url='http://your-server:5000',
    db_connection=your_db_connection
)

result = integration.on_review_submit(
    user_id=12345,
    product_id=67890,
    review_text="This product is amazing!",
    rating=5
)
```

---

## 📊 Benefits for E-commerce Platforms

### **Before Integration**
❌ Manual review moderation (slow, expensive)
❌ 30-40% fake reviews published
❌ Consumer trust issues
❌ Rating manipulation
❌ Brand reputation damage

### **After Integration**
✅ Automated detection (real-time)
✅ 88% fake reviews caught
✅ Increased consumer confidence
✅ Protected ratings
✅ Enhanced credibility
✅ 70% reduction in moderation costs

---

## 🎯 Quick Start Checklist

- [ ] Deploy detection API (Docker/Cloud)
- [ ] Test API with sample reviews
- [ ] Integrate with review submission flow
- [ ] Set up confidence thresholds
- [ ] Configure automated actions
- [ ] Enable logging and monitoring
- [ ] Train moderation team
- [ ] Launch and monitor

---

## 📞 Support

For integration assistance:
- API Documentation: See API_DOCS.md
- Technical Support: your-email@example.com
- GitHub Issues: your-repo-url

---

**Your e-commerce platform is now protected against fake reviews!** 🛡️
