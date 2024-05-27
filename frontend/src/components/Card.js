import { Card } from '@material-ui/core';
import {CardContent} from '@material-ui/core';
import {CardActionArea} from '@material-ui/core';
import {CardMedia} from '@material-ui/core';
import {Typography} from '@material-ui/core';
import React, { Component } from 'react';

export default function InfoCard(props) {
  return (
    <Card sx={{ maxWidth: 345 }}>
      <CardActionArea>
        <CardMedia
          component="img"
          height="140"
          image="../../static/images/codeTutor.png"
          alt="placeholder"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {props.header}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {props.description}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}