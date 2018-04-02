#ifndef ONEFLOW_CORE_OPERATOR_DECODE_RANDOM_OP_H_
#define ONEFLOW_CORE_OPERATOR_DECODE_RANDOM_OP_H_

#include "oneflow/core/operator/operator.h"

namespace oneflow {

class DecodeRandomOp final : public Operator {
 public:
  OF_DISALLOW_COPY_AND_MOVE(DecodeRandomOp);
  DecodeRandomOp() = default;
  ~DecodeRandomOp() = default;

  void InitFromOpConf() override;
  const PbMessage& GetCustomizedConf() const override;
  bool IsDecodeOp() const override { return true; }

  void InferBlobDescs(
      std::function<BlobDesc*(const std::string)> GetBlobDesc4BnInOp,
      const ParallelContext* parallel_ctx) const override;

 private:
  void VirtualGenKernelConf(
      std::function<const BlobDesc*(const std::string&)> GetBlobDesc4BnInOp,
      const ParallelContext* parallel_ctx,
      KernelConf* kernel_conf) const override;
};

}  // namespace oneflow

#endif  // ONEFLOW_CORE_OPERATOR_DECODE_RANDOM_OP_H_
