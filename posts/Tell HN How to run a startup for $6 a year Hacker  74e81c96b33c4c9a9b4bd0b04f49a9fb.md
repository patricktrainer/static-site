# Tell HN: How to run a startup for $6 a year | Hacker News

Created: Jul 20, 2020 2:17 AM
URL: https://news.ycombinator.com/item?id=22354060

Use this stack.

1. DynamoDB for database

2. AWS Lambda for backend

3. Netlify / Now / Surge for frontend

4. S3 for file/image hosting

5. Cloudinary for image hosting

6. IFTTT to webhook for cron

7. RedisLabs for queues, cache

8. Figma for designing and prototyping

9. Porkbun for $6 .com domains

10. Cloudflare for DNS

This setup is enough to handle ~1M/requests month, more or less, depending on the application.

If you are getting more traffic than that, your startup will be making money so you won’t mind upgrading. :)