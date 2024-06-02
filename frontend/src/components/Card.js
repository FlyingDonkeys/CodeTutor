import { Card } from '@material-ui/core';
import {CardContent} from '@material-ui/core';
import {CardActionArea} from '@material-ui/core';
import {CardMedia} from '@material-ui/core';
import {Typography} from '@material-ui/core';
import { Link } from '@mui/material';
import React, { Component } from 'react';

export default function InfoCard(props) {
  return (
    <Card sx={{ maxWidth: 345 }} style={{minHeight:'45vh'}}>
      <CardActionArea>
        <CardMedia
          component="img"
          height="140"
          image={props.link || "../../static/images/codeTutor.png"}
          alt="placeholder"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {props.header}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {props.description}
          </Typography>
          {props.path != "" ?
          <Link href ={props.path}>click here</Link>
          :null
          }
        </CardContent>
      </CardActionArea>
    </Card>
  );
}