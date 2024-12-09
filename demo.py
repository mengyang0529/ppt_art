from timeline.timeline import Timeline
import argparse

def main(args):
    t = Timeline.Style2(args.input)
    t.save_ppt(args.output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a PowerPoint presentation from a Markdown file.")
    parser.add_argument('--input', '-i', required=True, help="Path to the input Markdown file.")
    parser.add_argument('--output', '-o', required=True, help="Path to save the generated PPTX file.")
    args = parser.parse_args()
    main(args)
