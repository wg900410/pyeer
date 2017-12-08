# -*- coding:utf-8 -*-

import argparse

from os.path import join

import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

from .cmc_stats import load_scores_from_file, get_cmc_curve

__copyright__ = 'Copyright 2017'
__author__ = u'Manuel Aguado Martínez'


def get_cmc_info():
    # Setting script arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True, help="path to match files")
    ap.add_argument("-s", "--score_file_names", required=True,
                    help="Match scores file names separated by comma")
    ap.add_argument("-t", "--true_pairs_file_names", required=True,
                    help="True templates file names separated by comma")
    ap.add_argument("-e", "--experiment_names", required=True,
                    help="Experiment names separated by comma")
    ap.add_argument("-r", "--maximum_rank", required=False, default=20,
                    help="The maximum rank to calculate the penetration"
                         " coefficient. (default=20)")
    ap.add_argument("-lw", "--line_width", required=False, default=5,
                    help="The width of the plotted curves (default=5)")
    ap.add_argument("-lf", "--legend_font", required=False, default=20,
                    help="The size of the legend font (default=20)")
    args = ap.parse_args()

    # Parsing script arguments
    score_filenames = args.score_file_names.split(',')
    true_pairs_filenames = args.true_pairs_file_names.split(',')
    experiment_names = args.experiment_names.split(',')
    experiments = zip(score_filenames, true_pairs_filenames, experiment_names)
    rank = int(args.maximum_rank)
    line_width = int(args.line_width)
    legend_font = int(args.legend_font)

    # Preparing plots
    plt.title('CMC Curves')
    plt.ylabel('Accuracy')
    plt.xlabel('Rank')
    plt.grid(True)
    plt.axis(xmin=1, xmax=rank)
    plt.xticks(range(1, rank))

    # Calculating CMC values for each experiment and plotting them
    for exp in experiments:
        s_filename = join(args.path, exp[0])
        tp_filename = join(args.path, exp[1])
        experiment_name = exp[2]

        scores = load_scores_from_file(s_filename, tp_filename)
        ranks_values = get_cmc_curve(scores, rank)

        plt.plot(range(1, len(ranks_values) + 1), ranks_values,
                 label=experiment_name, linewidth=line_width)

    # Finalizing plots
    plt.legend(loc='best', prop=font_manager.FontProperties(size=legend_font))
    plt.show()
