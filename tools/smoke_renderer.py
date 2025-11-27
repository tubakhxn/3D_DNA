from renderer.dna_model import DNAModel


def main():
    m = DNAModel(stack_height=6.0, segments=36, radius=0.3)
    print('DNAModel instantiated')
    print('stack_height:', m.stack_height)
    print('segments:', m.segments)
    template = m.stack_template
    print('template keys:', list(template.keys()))
    a = template['strand_a']
    b = template['strand_b']
    print('strand_a shape:', a.shape)
    print('strand_b shape:', b.shape)
    # apply transforms without invoking GL
    ta = m._apply_twist_uncoil(a, 0, position_x= -1.0)
    tb = m._apply_twist_uncoil(b, 1, position_x= 1.0)
    print('transformed shapes:', ta.shape, tb.shape)
    # sanity-check some coordinates
    print('first point A:', ta[0])
    print('first point B:', tb[0])


if __name__ == '__main__':
    main()
