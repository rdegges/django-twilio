from twilio import Conference, Dial, Response
from django_twilio.decorators import twilio_view


@twilio_view
def conference(request, name, muted=None, beep=None,
		start_conference_on_enter=None, end_conference_on_exit=None,
		wait_url=None, wait_method=None, max_participants=None):
	"""A fully featured conference room.

	:param str name: Account-wide unique conference name. Callers who enter
		conference rooms with the same name will be placed into the same
		conference room.
	:param bool muted: Determines whether or not the caller can speak on in the
		conference room.
	:param bool beep: Determines whether or not a notification beep is played
		to the conference room when a participant joins or leaves the
		conference.
	:param bool start_conference_on_enter: Determines whether or not the
		conference will start when this participant joins the conference, if
		not already started.
	:param bool end_conference_on_exit: If a participant has this attribute set
		to true, then when that participant leaves, the conference ends and all
		other participants drop out.
	:param str wait_url: A URL for music that plays before the conference has
		started. The URL may be an MP3, a WAV, or a TwiML document that uses
		``<Play>`` or ``<Say>`` for content.
	:param str wait_method: The type of HTTP method to use when requesting
		``wait_url``. Defaults to 'POST'. Be sure to use 'GET' if you are
		directly requesting static audio files such as WAV or MP3 files so that
		twilio properly caches the files.
	:param int max_participants: This attribute indicates the maximum number of
		participants you want to allow within a named conference room. The
		default maximum number of participants is 40. The value must be a
		positive integer less than or equal to 40.

	Usage::

		# urls.py
		urlpatterns = patterns('',
			# ...
			url(r'^conference/?(P<name>\w+)/$', 'django_twilio.views.conference',
					{'max_participants': 10}),
			# ...
		)
	"""
	r = Response()
	d = Dial()
	d.append(Conference(
		name = name,
		muted = muted,
		beep = beep,
		startConferenceOnEnter = start_conference_on_enter,
		endConferenceOnExit = end_conference_on_exit,
		waitUrl = wait_url,
		waitMethod = wait_method,

		# TODO: Add in the max_participants attribute. Currently, the twilio
		# library doesn't support this attribute. I've sent them a pull request
		# to add it, but until that happens and they make a new PyPI release,
		# we'll have to do without it!
	))
	r.append(d)
	return r
