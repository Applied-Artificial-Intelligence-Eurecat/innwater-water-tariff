import { Component, ElementRef, OnInit, ViewChild, inject } from '@angular/core';
import * as d3 from 'd3';
import { ScatterPlotDataService } from '../scatter-plot-data.service';  // Assure-toi du chemin
import { CommonModule } from '@angular/common';
import { ScatterData } from './plot-data.interface';  // Assure-toi du chemin

@Component({
  selector: 'app-scatter-plot',
  //standalone: true,
 // imports: [CommonModule], // Ajout de CommonModule pour Angular Standalone
  template: `<div #chartContainer class="chart-container"></div>`,
  styles: [`
    .chart-container {
      width: 100%;
      height: 600px;
    }
  `]
})
export class ScatterPlotComponent implements OnInit {
  @ViewChild('chartContainer', { static: true }) chartContainer!: ElementRef;
  private scatterPlotDataService = inject(ScatterPlotDataService);  // Injection du bon service

  ngOnInit() {
    this.scatterPlotDataService.getPlotDataIterable().subscribe((data: ScatterData) => {
      this.createChart(data);
    });
  }

  private createChart(data: ScatterData) {
    const element = this.chartContainer.nativeElement;
    d3.select(element).selectAll('*').remove();  // Nettoyer le conteneur

    const margin = { top: 20, right: 30, bottom: 50, left: 50 },
          width = element.clientWidth - margin.left - margin.right,
          height = 600 - margin.top - margin.bottom;

    const svg = d3.select(element)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Définition des axes
    const x = d3.scaleLinear()
      .domain([0, d3.max(data.x)!])
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data.y)!])
      .range([height, 0]);

    const xAxis = d3.axisBottom(x);
    const yAxis = d3.axisLeft(y);

    // Ajouter les axes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(xAxis);

    svg.append('g')
      .call(yAxis);

    // Ajouter les points du nuage
    svg.selectAll('circle')
      .data(data.x.map((xValue, i) => ({ x: xValue, y: data.y[i] })))
      .enter()
      .append('circle')
      .attr('cx', d => x(d.x))
      .attr('cy', d => y(d.y))
      .attr('r', 5)
      .attr('fill', 'blue');

    // Ajout des seuils (lignes)
    svg.append('line') // Seuil vertical (800)
      .attr('x1', x(800)).attr('x2', x(800))
      .attr('y1', y(0)).attr('y2', y(25))
      .attr('stroke', 'red')
      .attr('stroke-dasharray', '5,5');

    svg.append('line') // Seuil horizontal (3)
      .attr('x1', x(0)).attr('x2', x(2000))
      .attr('y1', y(3)).attr('y2', y(3))
      .attr('stroke', 'green')
      .attr('stroke-dasharray', '5,5');
  }
}
