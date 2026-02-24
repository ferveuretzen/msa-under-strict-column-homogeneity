from functools import reduce, partial
from torchvision import models
from sch_msa.transform import align2merge, merged2aligned


def layers2list(model):
    return [m for m in model.modules() if len(list(m.children())) == 0]  # extract mainstream


def compare_names(module1, module2):
    return type(module1) is type(module2)


def compare_parameters(module1, module2):
    return str(module1) == str(module2)


def main():
    modules1 = layers2list(models.resnet50(weights=None))
    modules2 = layers2list(models.wide_resnet50_2(weights=None))
    modules3 = layers2list(models.resnext50_32x4d(weights=None))

    # align by module name, with ResNet50, Wide ResNet50, and ResNetXt

    custom_align2merge = partial(align2merge, compfunc=compare_names)

    merged_layers = reduce(custom_align2merge, [modules1, modules2, modules3])

    aligned_modules1 = merged2aligned(merged_layers, modules1, None, compfunc=compare_names)
    aligned_modules2 = merged2aligned(merged_layers, modules2, None, compfunc=compare_names)
    aligned_modules3 = merged2aligned(merged_layers, modules3, None, compfunc=compare_names)

    merged_strings = [type(m).__name__ if m is not None else "" for m in merged_layers]

    aligned_strings1 = [type(m).__name__ if m is not None else "" for m in aligned_modules1]
    aligned_strings2 = [type(m).__name__ if m is not None else "" for m in aligned_modules2]
    aligned_strings3 = [type(m).__name__ if m is not None else "" for m in aligned_modules3]

    width = len(max(merged_strings, key=len))
    depth = len(str(len(merged_strings)))

    OUT_PATH = "examples/aligned_resnet_by_name.out"

    with open(OUT_PATH, "w") as fp:
        print("Depth".ljust(depth + len("[]")), "ResNet50".ljust(width), "Wide ResNet50".ljust(width), "ResNetXt".ljust(width), file=fp)

        for j in range(len(merged_layers)):
            print(
                f"[{str(j).rjust(depth)}]",
                aligned_strings1[j].ljust(width),
                aligned_strings2[j].ljust(width),
                aligned_strings3[j].ljust(width),
                file=fp,
            )

    # align by module name and parameters, with ResNet50, Wide ResNet50, and ResNetXt

    custom_align2merge = partial(align2merge, compfunc=compare_parameters)

    merged_layers = reduce(custom_align2merge, [modules1, modules2, modules3])

    aligned_modules1 = merged2aligned(merged_layers, modules1, "", compfunc=compare_parameters)
    aligned_modules2 = merged2aligned(merged_layers, modules2, "", compfunc=compare_parameters)
    aligned_modules3 = merged2aligned(merged_layers, modules3, "", compfunc=compare_parameters)

    merged_strings = [str(m) for m in merged_layers]

    aligned_strings1 = [str(m) for m in aligned_modules1]
    aligned_strings2 = [str(m) for m in aligned_modules2]
    aligned_strings3 = [str(m) for m in aligned_modules3]

    width = len(max(merged_strings, key=len))
    depth = len(str(len(merged_strings)))

    OUT_PATH = "examples/aligned_resnet_by_parameters.out"

    with open(OUT_PATH, "w") as fp:
        print("Depth".ljust(depth + len("[]")), "ResNet50".ljust(width), "Wide ResNet50".ljust(width), "ResNetXt".ljust(width), file=fp)

        for j in range(len(merged_layers)):
            print(
                f"[{str(j).rjust(depth)}]",
                aligned_strings1[j].ljust(width),
                aligned_strings2[j].ljust(width),
                aligned_strings3[j].ljust(width),
                file=fp,
            )


if __name__ == "__main__":
    main()
