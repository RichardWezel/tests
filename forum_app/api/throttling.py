from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class QuestionThrottle(UserRateThrottle):
    scope = 'question'

    def allow_request(self, request, view):

        if request.method == 'GET':
            # Allow GET requests without throttling
            return True
        
        new_scope = 'question-' + request.method.lower()
        if new_scope in self.THROTTLE_RATES:
            self.scope = new_scope
            self.rate = self.get_rate()
            self.num_requests, self.duration = self.parse_rate(self.rate)
            print(f"Throttling scope set to: {self.scope}")

        return super().allow_request(request, view)

