import { Component, AfterViewInit, ElementRef, ViewChild } from '@angular/core';
import { PenParadeDataService, ScatterData } from '../PenParadeDataService';
import * as d3 from 'd3';

@Component({
  selector: 'app-pen-parade-chart',
  templateUrl: './pen-parade-chart.component.html',
  styleUrls: ['./pen-parade-chart.component.css']
})
export class PenParadeChartComponent implements AfterViewInit {
  @ViewChild('chart', { static: false }) private chartContainer!: ElementRef;
  baseData: ScatterData[] = [];
  captiveData: ScatterData[] = [];

  constructor(private dataService: PenParadeDataService) {}

  ngAfterViewInit(): void {
    console.log("Conteneur du graphique :", this.chartContainer);
    if (!this.chartContainer) {
      console.error("Le conteneur du graphique n'a pas été trouvé !");
      return;
    }
    this.loadDataAndCreateChart();
  }

  private loadDataAndCreateChart(): void {
    this.dataService.getPlotData().subscribe({
      next: (data) => {
        this.baseData = data.base;
        this.captiveData = data.captive;

        console.log("Base Data:", this.baseData);
        console.log("Captive Data:", this.captiveData);

        this.createChart(); // Crée le graphique une fois les données chargées
      },
      error: (err) => console.error("Erreur lors de la récupération des données :", err)
    });
  }

  private createChart(): void {
    if (!this.chartContainer) {
      console.error("Conteneur du graphique non trouvé !");
      return;
    }

    const element = this.chartContainer.nativeElement;
    d3.select(element).selectAll('*').remove();  // Nettoie le conteneur

    const width = 800, height = 600; // Nouvelle taille du SVG
    const svg = d3.select(element)
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    console.log("SVG créé :", svg.node());

    // Définir les échelles
    const xScale = d3.scaleLinear()
      .domain([0, 1])
      .range([50, width - 50]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max([...this.baseData, ...this.captiveData], d => d.y) || 1])
      .range([height - 50, 50]);

    console.log("Domaine de xScale :", xScale.domain());
    console.log("Domaine de yScale :", yScale.domain());

    // Ajouter l'axe des abscisses (X)
    svg.append('g')
      .attr('transform', `translate(0, ${height - 50})`)
      .call(d3.axisBottom(xScale));

    // Ajouter l'axe des ordonnées (Y)
    svg.append('g')
      .attr('transform', 'translate(50, 0)')
      .call(d3.axisLeft(yScale));

    // Légende pour l'axe des abscisses (X)
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', height - 10)
      .style('text-anchor', 'middle')
      .text('Axe des X');

    // Légende pour l'axe des ordonnées (Y)
    svg.append('text')
      .attr('transform', 'rotate(-90)')
      .attr('x', -height / 2)
      .attr('y', 20)
      .style('text-anchor', 'middle')
      .text('Axe des Y');

    // Ajouter une légende pour les points
    const legend = svg.append('g')
      .attr('transform', `translate(${width - 150}, 20)`);

    // Légende pour les consommations de base (bleu)
    legend.append('rect')
      .attr('x', 0)
      .attr('y', 0)
      .attr('width', 10)
      .attr('height', 10)
      .style('fill', 'blue');

    legend.append('text')
      .attr('x', 20)
      .attr('y', 10)
      .style('text-anchor', 'start')
      .text('Consommations de base');

    // Légende pour les consommations captives (rouge)
    legend.append('rect')
      .attr('x', 0)
      .attr('y', 20)
      .attr('width', 10)
      .attr('height', 10)
      .style('fill', 'red');

    legend.append('text')
      .attr('x', 20)
      .attr('y', 30)
      .style('text-anchor', 'start')
      .text('Consommations captives');

    // Tooltip
    const tooltip = d3.select('#tooltip');

    // Tracer les points "base" (bleus)
    svg.selectAll('circle.base')
      .data(this.baseData)
      .enter()
      .append('circle')
      .attr('cx', d => xScale(d.x))
      .attr('cy', d => yScale(d.y))
      .attr('r', 5)
      .style('fill', 'blue')
      .on('mouseover', (event, d) => {
        tooltip.transition().duration(200).style('opacity', 1);
        tooltip.html(`X: ${d.x}<br>Y: ${d.y}`)
          .style('left', `${event.pageX + 5}px`)
          .style('top', `${event.pageY - 20}px`);
      })
      .on('mouseout', () => {
        tooltip.transition().duration(500).style('opacity', 0);
      });

    // Tracer les points "captive" (rouges)
    svg.selectAll('circle.captive')
      .data(this.captiveData)
      .enter()
      .append('circle')
      .attr('cx', d => xScale(d.x))
      .attr('cy', d => yScale(d.y))
      .attr('r', 5)
      .style('fill', 'red')
      .on('mouseover', (event, d) => {
        tooltip.transition().duration(200).style('opacity', 1);
        tooltip.html(`X: ${d.x}<br>Y: ${d.y}`)
          .style('left', `${event.pageX + 5}px`)
          .style('top', `${event.pageY - 20}px`);
      })
      .on('mouseout', () => {
        tooltip.transition().duration(500).style('opacity', 0);
      });
  }
}