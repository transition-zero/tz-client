#!/usr/bin/env python

import click


@click.group()
@click.pass_context
def root(ctx):
    """TransitionZero FEO Client CLI."""
