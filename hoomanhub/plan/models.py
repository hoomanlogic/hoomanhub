from django.db import models
from datetime import timedelta, datetime, date
from core.models import TimeStampedModel, UniquelyNamedModel, ArchiveableModel, DocumentableModel, TaggableModel


#=======================================================================================================================
# Models
#=======================================================================================================================
class Action(TimeStampedModel, UniquelyNamedModel, ArchiveableModel, DocumentableModel, TaggableModel):
    STATUS = ((0, 'CURRENT'), (1, 'FUTURE'), (2, 'COMPLETE'))
    status = models.PositiveIntegerField(choices=STATUS, default=0)
    #imgheight = models.IntegerField(blank=True, null=True)
    #imgwidth = models.IntegerField(blank=True, null=True)
    #imgurl = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('action-detail', kwargs={'pk': self.pk})

    @property
    def statusdesc(self):
        if self.status == 0:
            return 'Current'
        elif self.status == 1:
            return 'Future'
        elif self.status == 2:
            return 'Complete'
        return ''

    @property
    def total_executions(self):
        return self.execution_set.count()

    @property
    def current_percentage(self):
        return self.execution_set.sum('percentage')

    @property
    def total_minutes(self):
        return self.execution_set.sum('minutes')


class Decision(TimeStampedModel):
    conditions = models.TextField()


# Share Tags: #tinyadventure: estimated time,
class Flow(TimeStampedModel, UniquelyNamedModel, ArchiveableModel, DocumentableModel, TaggableModel):
    FLOW_TYPE = ((0, 'queue'), (1, 'block'), (2, 'option'), (3, 'factory'), (4, 'routine'))
    flow_type = models.PositiveSmallIntegerField(choices=FLOW_TYPE)


class FlowIndex(TimeStampedModel):
    INDEX_TYPE = ((0, 'action'), (1, 'flow'), (2, 'decision'))
    parent = models.ForeignKey('Flow', related_name='children')
    index = models.PositiveIntegerField()
    action = models.ForeignKey('Action', related_name='flow_indexes', blank=True, null=True)
    flow = models.ForeignKey('Flow', related_name='flow_indexes', blank=True, null=True)
    decision = models.ForeignKey('Decision', related_name='flow_indexes', blank=True, null=True)

    #todo: must validate that action, flow, OR decision is set, but not more than one of them


class Tag(TimeStampedModel, ArchiveableModel, DocumentableModel):
    TAG_TYPE = ((0, 'standard'), (1, 'focus'), (2, 'reason'), (3, 'need'), (4, 'plan'))
    name = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    type = models.PositiveIntegerField(choices=TAG_TYPE, default=0)

    def __unicode__(self):
        return self.name


class Block(TimeStampedModel, UniquelyNamedModel, ArchiveableModel, DocumentableModel):
    pass


class BlockTag(TimeStampedModel):
    FILTER_TYPE = ((0, 'exclude'), (1, 'include'))
    block = models.ForeignKey('Block')
    tag = models.ForeignKey('Tag')
    filter = models.PositiveSmallIntegerField(choices=FILTER_TYPE)


class Target(TimeStampedModel, ArchiveableModel):
    action = models.ForeignKey('Action', related_name='targets', blank=True, null=True)
    flow = models.ForeignKey('Flow', related_name='targets', blank=True, null=True)
    tag = models.ForeignKey('Tag', related_name='targets', blank=True, null=True)
    MEASURE_TYPE = ((0, 'executions'), (1, 'percentage'), (2, 'minutes'))
    FREQUENCY = ((0, 'yearly'), (1, 'monthly'), (2, 'weekly'), (3, 'daily'), (4, 'once'), (5, 'dates'))
    freq = models.PositiveSmallIntegerField(choices=FREQUENCY)
    measure = models.PositiveSmallIntegerField(choices=MEASURE_TYPE)
    interval = models.PositiveSmallIntegerField()
    starts = models.DateField()
    off_interval = models.PositiveSmallIntegerField()
    period_target = models.IntegerField()
    met_after = models.IntegerField()
    break_after = models.PositiveSmallIntegerField()
    break_freq = models.PositiveSmallIntegerField(choices=FREQUENCY)
    break_interval = models.PositiveSmallIntegerField()

    #todo: must validate that action, flow, OR tag is set, but not more than one of them

    #===================================================================================================================
    # string formatting properties
    #===================================================================================================================
    @property
    def measure_symbol(self):
        if self.measure == 0:
            return ''
        elif self.measure == 1:
            return '%'
        elif self.measure == 2:
            return 'min'

    @property
    def period_target_desc(self):
        if self.measure != 2:
            return "{}{}".format(self.period_target, self.measure_symbol)
        else:
            return Duration.minutes_to_duration(self.period_target)

    @property
    def period_desc(self):
        dtfrom, dtto = self.get_current_period()
        if dtfrom == dtto:
            return str(dtfrom)
        else:
            return "{} - {}".format(dtfrom, dtto)

    @property
    def progress(self):
        history = self.model.history.sort('timestamp').flip()

        period_from, period_to = self.get_period(datetime.today().date())

        count = 0
        progress = 0
        minutes = 0

        for log in history:
            if period_from <= log.logdate <= period_to:
                count += 1
                if log.progress is not None:
                    progress += log.progress
                if log.minutes is not None:
                    minutes += log.minutes
            elif log.logdate < period_from:
                break

        if self.measure == 0:
            return "{}/{}".format(count, self.period_target)
        elif self.measure == 1:
            return "{}/{}{}".format(progress, self.period_target, self.measure_symbol)
        elif self.measure == 2:
            return "{}/{}".format(Duration.minutes_to_duration(minutes),
                                  Duration.minutes_to_duration(self.period_target))

    @property
    def daysleft(self):
        period_from, period_to = self.get_period(datetime.today().date())

        daysleft = (period_to - datetime.today().date()).days + 1  # including today
        dayspassed = (datetime.today().date() - period_from).days
        daystotal = (period_to - period_from).days + 1  # including today
        return "{}/{}/{}".format(dayspassed, daysleft, daystotal)

    #===================================================================================================================
    # calculated properties
    #===================================================================================================================
    @property
    def average(self):

        history = self.model.history.sort('timestamp')

        periods = {}

        target = len(self.periods[:-1]) * self.period_target
        actual = 0

        history_enumerator = enumerate(history)

        try:
            logstepper, log = history_enumerator.next()
        except StopIteration:
            log = None

        for period in self.periods[:-1]:
            dtfrom, dtto = period
            periods[(dtfrom.strftime("%Y-%m-%d"), dtfrom, dtto)] = 0

            while log is not None and log.logdate <= dtto:
                if dtfrom <= log.logdate <= dtto:
                    periods[(dtfrom.strftime("%Y-%m-%d"), dtfrom, dtto)] += self._add_log_progress(log)
                try:
                    logstepper, log = history_enumerator.next()
                except StopIteration:
                    log = None

            actual += periods[(dtfrom.strftime("%Y-%m-%d"), dtfrom, dtto)]

        if actual == 0 or target == 0:
            return "0%"
        else:
            return "{:.2f}%".format((float(actual) / float(target)) * 100)

    @property
    def thisperiod(self):

        history = self.model.history.sort('timestamp')
        target = self.period_target
        actual = 0

        history_enumerator = enumerate(history)

        try:
            logstepper, log = history_enumerator.next()
        except StopIteration:
            log = None

        dtfrom, dtto = self.periods[-1]

        while log is not None and log.logdate <= dtto:
            if dtfrom <= log.logdate <= dtto:
                actual += self._add_log_progress(log)
            try:
                logstepper, log = history_enumerator.next()
            except StopIteration:
                log = None

        if actual == 0 or target == 0:
            return "0%"
        else:
            return "{:.2f}%".format((float(actual) / float(target)) * 100)

    #===================================================================================================================
    # calculated methods
    #===================================================================================================================
    def get_period(self, dateobj):

        for period in self.periods:
            dtfrom, dtto = period
            if dtfrom <= dateobj <= dtto:
                return dtfrom, dtto

        # no current periods, get last period
        if len(self.periods) > 0:
            dtfrom, dtto = self.periods[-1]
            return dtfrom, dtto
        else:
            return None, None

    def get_current_period(self):
        period_from, period_to = self.periods[-1]
        return period_from, period_to

    def get_last_execution_date(self):
        return self.model.get_last_execution_date()

    def calculate_periods(self, uptodate):

        periods = []
        periodcount = 0
        dtfrom = self.starts
        dtto = None

        while dtfrom <= uptodate:
            dtfrom, dtto = self.calculate_period(dtfrom, periodcount)

            # returns none when at end of target lifespan
            if dtfrom is None or dtto is None:
                break

            # catch when there are no more periods and it continues passing the last period
            if dtfrom > dtto or (dtfrom, dtto) in periods:
                break

            periods.append((dtfrom, dtto))
            dtfrom = dtto + timedelta(days=1)
            periodcount += 1

        return periods

    def calculate_period(self, relativedate, periodcount):
        periodfrom = relativedate

        if self._ends_ is not None and relativedate > self._ends_:
            return None, None

        # break periods
        if periodcount > 0 and self.breakafter is not None and self.breakafter > 0:
            if self.breakafter % periodcount == 0:
                periodfrom, periodto = self._calculate_period(periodfrom, self.breakfreq, self.breakinterval, 0, periodcount)
                periodfrom = periodto + timedelta(days=1)

        periodfrom, periodto = self._calculate_period(periodfrom, self.freq, self.interval, self.offinterval, periodcount)

        return periodfrom, periodto

    def _calculate_period(self, relativedate, freq, interval, offinterval, periodcount):

        periodfrom = relativedate
        periodto = None

        # push off period based on offinterval
        if offinterval > 0 and periodcount > 0:
            periodfrom, periodto = self._calculate_period(periodfrom, freq, offinterval, 0, periodcount)
            periodfrom = periodto + timedelta(days=1)

        if freq < 4:
            trueinterval = interval - offinterval

        if freq == Target.YEARLY:
            if periodfrom.day != 1 or periodfrom.month != 1:
                periodfrom = Target.todate("{}-{:0>2}-{:0>2}".format(periodfrom.year, 1, 1))
            periodto = Target.todate("{}-{:0>2}-{:0>2}".format(periodfrom.year + (trueinterval - 1), 12, 31))

        elif freq == Target.MONTHLY:
            if periodfrom.day != 1:
                periodfrom = Target.todate("{}-{:0>2}-{:0>2}".format(periodfrom.year, periodfrom.month, 1))
            if periodfrom.month + trueinterval <= 12:
                periodto = Target.todate("{}-{:0>2}-{:0>2}".format(
                    periodfrom.year, periodfrom.month + trueinterval, periodfrom.day))
            else:
                periodto = Target.todate("{}-{:0>2}-{:0>2}".format(
                    periodfrom.year + 1, trueinterval - (12 - periodfrom.month), periodfrom.day))
            periodto -= timedelta(days=1)

        elif freq == Target.WEEKLY:
            if periodfrom.weekday() != 0:
                periodfrom = periodfrom - timedelta(days=periodfrom.weekday())
            periodto = periodfrom + timedelta(weeks=1*trueinterval, days=-1)

        elif freq == Target.DAILY:
            periodto = periodfrom + timedelta(days=trueinterval - 1)

        elif freq == Target.ONCE:
            periodto = self.interval

        elif freq == Target.DATES:
            periodto = self._get_next_date_interval(periodfrom)

        return periodfrom, periodto

    def _get_next_date_interval(self, relativedate):
        for dt in self.interval:
            if dt >= relativedate:
                return dt
        return None

    def _add_log_progress(self, log):

        if self.measure == 0:
            return 1
        elif self.measure == 1 and log.progress is not None:
            return log.progress
        elif self.measure == 2 and log.minutes is not None:
            return log.minutes
        else:
            return 0


class Execution(models.Model):
    root_flow = models.ForeignKey('Flow', related_name='root_executions', blank=True, null=True)
    parent_flow = models.ForeignKey('Flow', related_name='parent_executions', blank=True, null=True)
    action = models.ForeignKey('Action')
    percentage = models.SmallIntegerField(default=100)
    minutes = models.PositiveIntegerField(default=0)


class Phase(TimeStampedModel, UniquelyNamedModel, ArchiveableModel, DocumentableModel, TaggableModel):
    # uses dateutil.rrule freq, dtstart=None,
    #                 interval=1, wkst=None, count=None, until=None, bysetpos=None,
    #                 bymonth=None, bymonthday=None, byyearday=None, byeaster=None,
    #                 byweekno=None, byweekday=None,
    #                 byhour=None, byminute=None, bysecond=None
    FREQUENCY = ((0, "YEARLY"), (1, "MONTHLY"), (2, "WEEKLY"), (3, "DAILY"), (4, "HOURLY"), (5, "MINUTELY"),
                 (6, "SECONDLY"))
    freq = models.PositiveSmallIntegerField(choices=FREQUENCY)
    dtstart = models.DateField()
    interval = models.PositiveIntegerField(default=1)
    until = models.DateField(blank=True, null=True)
    count = models.PositiveIntegerField(blank=True, null=True)
    bysetpos = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    bymonth = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    bymonthday = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    byyearday = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    byweekno = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    byweekday = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    byhour = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    byminute = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    bysecond = models.CommaSeparatedIntegerField(max_length=100, blank=True, null=True)
    timefrom = models.PositiveIntegerField(blank=True, null=True)
    timeto = models.PositiveIntegerField(blank=True, null=True)


class Cycle(TimeStampedModel, UniquelyNamedModel, DocumentableModel):
    phases = models.ManyToManyField('Phase', blank=True)
