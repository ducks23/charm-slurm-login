#! /usr/bin/env python3
"""SlurmdbdProvidesRelation."""
import logging
import json
from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
)


logger = logging.getLogger()


class ConfigAvailableEvents(EventBase):
    logger.debug("config available event emmitted ######")

class LoginEvents(ObjectEvents):
    config_available = EventSource(ConfigAvailableEvents)


class LoginRequires(Object):
    """SlurmdbdProvidesRelation."""

    on = LoginEvents()
    def __init__(self, charm, relation_name):
        """Set the provides initial data."""
        super().__init__(charm, relation_name)
        self.charm = charm
        self.framework.observe(
            charm.on[relation_name].relation_changed,
            self._on_relation_changed
        )
    def _on_relation_changed(self, event):
        config = event.relation.data[event.unit].get("slurm_config", None)
        self.charm._stored.slurm_config = json.loads(config)
        self.on.config_available.emit()
